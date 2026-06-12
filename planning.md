# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is The Unofficial Guide to the Queens College Computer Science student experience. This system will help students find information about the CS department, required courses, recommended course sequence, professors, clubs, and career resources. This knowledge is valuable because official pages explain requirements, but they do not always explain what the student experience is like, which professors students recommend, or how students actually navigate the major.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

  | # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Queens College Computer Science Department | Official overview of the Computer Science department, academic programs, research, and department mission. | https://www.cs.qc.cuny.edu/ |
| 2 | Queens College Undergraduate Computer Science Courses | Official descriptions of undergraduate Computer Science courses, including course objectives and topics covered. | https://www.cs.qc.cuny.edu/index-1.html |
| 3 | Queens College Computer Science BS 4-Year Plan | Recommended semester-by-semester course sequence for students pursuing the Bachelor of Science in Computer Science. | https://www.qc.cuny.edu/aac/wp-content/uploads/sites/84/2022/12/Computer-Science-BS-4-Year-Plan.pdf |
| 4 | Queens College Computer Science BS Degree Requirements | Official degree requirements, required courses, electives, and graduation requirements for the Computer Science BS program. | https://www.cs.qc.cuny.edu/ |
| 5 | Queens College Computer Science Academic Advising | Information about academic advising, advisor contacts, registration guidance, and degree planning for Computer Science students. | https://www.cs.qc.cuny.edu/advisor.php |
| 6 | Queens College Computer Science Faculty | Faculty profiles, research interests, office locations, and contact information for Computer Science faculty members. | https://www.cs.qc.cuny.edu/faculty.html |
| 7 | Queens College Learning Commons – CSCI Resources & Tutoring | Provides free peer tutoring, CSCI review sessions, programming workshops, LeetCode practice, and academic support resources for Computer Science students. | https://www.qc.cuny.edu/academics/qclc/resources/ |
| 8 | RateMyProfessor – Anne Smith-Thompson | Student reviews discussing teaching style, workload, grading, course difficulty, and overall classroom experience. | https://www.ratemyprofessors.com/ |
| 9 | RateMyProfessor – Kenneth Lord | Student reviews discussing teaching style, workload, grading, course difficulty, and overall classroom experience. | https://www.ratemyprofessors.com/ |
| 10 | Queens College Career Development and Internships | Career services, internship opportunities, resume support, career fairs, and professional development resources available to Queens College students. | https://www.qc.cuny.edu/career-services/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:**

I will split each document into chunks of approximately 500 characters with a 100-character overlap between consecutive chunks. This size is appropriate because most of my documents contain short sections, course descriptions, faculty information, advising resources, and student reviews. Using a small overlap helps preserve context when important information spans two chunks, reducing the chance of losing relevant details during retrieval.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 (Sentence Transformers)

**Top-k:** 3

**Production tradeoff reflection:**

I chose the all-MiniLM-L6-v2 embedding model because it is lightweight, fast, and provides good semantic search performance for short and medium-length documents such as course descriptions, advising pages, faculty profiles, and student reviews. Retrieving the top 3 most relevant chunks should provide enough context for the language model without introducing too much unrelated information.

If this system were deployed for real users and cost was not a concern, I would consider using a larger embedding model with stronger semantic understanding and better support for longer documents. I would also consider multilingual support, retrieval accuracy, latency, and the ability to handle domain-specific terminology when selecting an embedding model.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->


| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What courses are recommended during the first semester of the Queens College Computer Science BS program? | The system should list the recommended first-semester courses from the BS 4-Year Plan, including English Composition I, World Cultures & Global Issues, U.S. Experience in its Diversity, Creative Expression, and Calculus I (MATH 151). |
| 2 | How can a Computer Science student contact an academic advisor? | The system should provide the academic advising information and advisor contact details from the Computer Science Advising page. |
| 3 | What topics are covered in CSCI 313 – Data Structures? | The system should explain that CSCI 313 covers data structures such as stacks, queues, trees, graphs, hash tables, searching, sorting, and algorithm analysis. |
| 4 | What tutoring and academic support resources are available for Computer Science students? | The system should mention the Learning Commons tutoring services, peer tutoring, CSCI review sessions, programming workshops, and LeetCode practice resources. |
| 5 | What do students say about Professor Anne Smith-Thompson's teaching style and workload? | The system should summarize the student reviews from RateMyProfessor, including comments about teaching style, workload, grading, and overall classroom experience. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some documents may be noisy or inconsistent. Official Queens College pages may contain navigation text, repeated headers, footers, or extra links, while RateMyProfessor pages may contain ads or short review fragments. I will need to clean the documents carefully so the system retrieves useful content instead of page clutter.

2. Retrieval may return partially relevant chunks if the question is too broad or if important information is split across chunk boundaries. For example, a course name may appear in one chunk while its description appears in the next chunk. I will use overlap between chunks and inspect sample chunks before embedding to reduce this issue.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->


                        User Question
                              │
                              ▼
                    Retrieve Relevant Chunks
                              ▲
                              │
                         ChromaDB Vector Store
                              ▲
                              │
                         Generate Embeddings
                         (all-MiniLM-L6-v2)
                              ▲
                              │
                         Chunk Documents
                    (500 characters, 100 overlap)
                              ▲
                              │
                         Document Ingestion
                    (Load and clean .txt documents)
                              ▲
                              │
                    Queens College CS Documents
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will use ChatGPT to help implement the document ingestion and chunking pipeline. I will provide my chunking strategy from this planning document, including the chunk size and overlap, and ask it to generate Python code to load my documents, clean the text, and split it into chunks. I will verify the output by checking that every document is loaded correctly and that the generated chunks have the expected size and overlap.

**Milestone 4 — Embedding and retrieval:**

I will use Claude to help implement the embedding and retrieval pipeline. I will provide my retrieval approach, including the embedding model, top-k retrieval value, and architecture diagram, and ask it to generate Python code to create embeddings, store them in ChromaDB, and retrieve the most relevant chunks for a user query. I will verify the implementation by testing multiple questions and confirming that the retrieved chunks are relevant and come from the appropriate source documents.

**Milestone 5 — Generation and interface:**

I will use ChatGPT to help implement the response generation pipeline and command-line interface. I will provide my project requirements, grounding strategy, and retrieval pipeline, and ask it to generate code that sends the retrieved context to the LLM and generates responses based only on the provided documents. I will verify the implementation by running my evaluation questions and checking that the responses are accurate, grounded in the retrieved documents, and do not include unsupported information.
