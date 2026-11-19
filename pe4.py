import wikipedia
import time
from concurrent.futures import ThreadPoolExecutor

wikipedia.set_user_agent(
    "IST303PairExercise/1.0 (https://github.com/amirstrongkhan/Pair-Exercise-4)"
)

wikipedia.set_rate_limiting(True)


# -------------------------
# SEARCH FOR TOPICS
# -------------------------

def search_topics():
    for attempt in range(3):
        try:
            topics = wikipedia.search("generative artificial intelligence")
            if not topics:
                raise SystemExit("Wikipedia returned no topics.")
            return topics
        except Exception as error:
            if attempt == 2:
                raise SystemExit(f"Wikipedia search failed: {error}") from error
            print("Wikipedia search failed. Retrying...")
            time.sleep(2)


# -------------------------
# SECTION A - SEQUENTIAL
# -------------------------

topics = search_topics()
print(topics)

start_time = time.perf_counter()

for each_topic in topics:
    print("Sequential downloading:", each_topic)

    for attempt in range(3):
        try:
            page = wikipedia.page(
                each_topic,
                auto_suggest=False
            )

            title = page.title
            references = page.references
            break

        except Exception as error:
            print(f"Download failed for {each_topic}: {error}")
            if attempt < 2:
                time.sleep(1)
    else:
        print("Could not download:", each_topic)
        continue

    try:
        filename = title + ".txt"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            for reference in references:
                file.write(reference + "\n")

    except Exception:
        print("Could not save:", each_topic)


end_time = time.perf_counter()

print(
    "Sequential time:",
    end_time - start_time
)


# -------------------------
# PAUSE BEFORE CONCURRENT
# -------------------------

print("Waiting before concurrent test...")
time.sleep(10)


# -------------------------
# SECTION B - CONCURRENT
# -------------------------

def wiki_dl_and_save(topic):

    print("Concurrent downloading:", topic)

    for attempt in range(3):

        try:
            page = wikipedia.page(
                topic,
                auto_suggest=False
            )

            title = page.title
            references = page.references
            break

        except Exception as error:
            print(f"Download failed for {topic}: {error}")
            if attempt < 2:
                time.sleep(1)
    else:
        print("Could not download:", topic)
        return

    try:
        filename = title + ".txt"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            for reference in references:
                file.write(reference + "\n")

    except Exception:
        print("Could not save:", topic)


# Repeat the search for Section B before timing the downloads.
wikipedia.search.clear_cache()
topics = search_topics()
print(topics)

start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=2) as executor:

    list(
        executor.map(
            wiki_dl_and_save,
            topics
        )
    )


end_time = time.perf_counter()

print(
    "Concurrent time:",
    end_time - start_time
)
