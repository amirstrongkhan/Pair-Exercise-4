import wikipedia
import time
from concurrent.futures import ThreadPoolExecutor

wikipedia.set_user_agent(
    "IST303 Pair Exercise 4 - student project"
)

wikipedia.set_rate_limiting(True)


# -------------------------
# SEARCH FOR TOPICS
# -------------------------

topics = None

for attempt in range(3):
    try:
        topics = wikipedia.search(
            "generative artificial intelligence"
        )
        break
    except Exception:
        print("Wikipedia search failed. Retrying...")
        time.sleep(2)

if topics is None:
    print("Wikipedia search could not be completed.")
    raise SystemExit

print(topics)


# -------------------------
# SECTION A - SEQUENTIAL
# -------------------------

start_time = time.perf_counter()

for each_topic in topics:
    print("Sequential downloading:", each_topic)

    page = None

    for attempt in range(3):
        try:
            page = wikipedia.page(
                each_topic,
                auto_suggest=False
            )

            title = page.title
            references = page.references
            break

        except Exception:
            print("Retrying:", each_topic)
            time.sleep(1)

    if page is None:
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

    page = None

    for attempt in range(3):

        try:
            page = wikipedia.page(
                topic,
                auto_suggest=False
            )

            title = page.title
            references = page.references
            break

        except Exception:
            print("Retrying:", topic)
            time.sleep(1)

    if page is None:
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