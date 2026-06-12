# The Unofficial Guide — Project 1
Sumbitted by: **Hisey Dolma Ghising**


## Demo Video

<div>
  <a href="https://www.loom.com/share/17ebe78483024ce9b5516b83aa62cb7b">
    <p><strong>🎥 Watch the Project Demo</strong></p>
  </a>
  <a href="https://www.loom.com/share/17ebe78483024ce9b5516b83aa62cb7b">
    <img style="max-width:500px;" src="https://cdn.loom.com/sessions/thumbnails/17ebe78483024ce9b5516b83aa62cb7b-70cfe57d670f9e8c-full-play.gif#t=0.1">
  </a>
</div>



## Domain

My project is an unofficial guide for Queens College Computer Science students. It brings together important information such as degree requirements, course information, faculty, academic advising, tutoring resources, career services, and AI internship opportunities into one place where students can ask questions and quickly find answers.

I chose this topic because a lot of useful information is spread across different Queens College websites, so it can take time to find what you're looking for. Instead of searching through multiple pages, students can simply ask a question and get an answer based on the documents collected for this project.


---

## Document Sources


| # | Source | Type | URL or File |
|---|--------|------|-------------|
| 1 | Queens College Computer Science Department | Official Website | https://www.cs.qc.cuny.edu/ |
| 2 | Queens College Undergraduate Computer Science Courses | Official Website | https://www.cs.qc.cuny.edu/index-1.html |
| 3 | Queens College Computer Science BS 4-Year Plan | PDF | https://www.qc.cuny.edu/aac/wp-content/uploads/sites/84/2022/12/Computer-Science-BS-4-Year-Plan.pdf |
| 4 | Queens College Computer Science BS Degree Requirements | PDF | https://www.cs.qc.cuny.edu/undergrad/BS_FA22.pdf |
| 5 | Queens College Computer Science Academic Advising | Official Website | https://www.cs.qc.cuny.edu/advisor.php |
| 6 | Queens College Computer Science Faculty | Official Website | https://www.qc.cuny.edu/academics/cs/faculty/ |
| 7 | Queens College Learning Commons – Computer Science Resources | Official Website | https://www.qc.cuny.edu/academics/qclc/resources/ |
| 8 | Queens College Center for Career Engagement and Internships (CEI) | Official Website | https://www.qc.cuny.edu/academics/cei/ |
| 9 | AI Skill Foundry – 3-Hour Micro-Internship | Official Website | https://aiskillfoundry.com/3hmi-application |
| 10 | Queens College Computer Science Student Resources | Official Website | https://www.cs.qc.cuny.edu/index-5.html |

---

## Chunking Strategy

**Chunk size:**  
400 characters

**Overlap:**  
80 characters

**Why these choices fit your documents:**  
Most of my documents are short to medium-length text files, so a 400-character chunk was enough to keep related information together without making each chunk too large. I used an 80-character overlap so information at the boundary between two chunks wouldn't be lost. Before chunking, I manually cleaned the documents by removing unnecessary webpage content such as navigation menus, headers, and other text that wasn't useful for answering questions. The documents were then saved as plain `.txt` files.

**Final chunk count:**  
53 chunks across 10 documents.

---

## Embedding Model

**Model used:**  
I used **all-MiniLM-L6-v2** from the `sentence-transformers` library to generate embeddings for each document chunk.

**Production tradeoff reflection:**  
I chose this model because it runs locally, is free to use, and is fast enough for a small project like this. If I were building this for real users, I would also consider using a larger embedding model that could provide better retrieval accuracy, especially for longer or more complex documents. The tradeoff is that larger models usually require more computing power, have higher latency, and may require paid API access. Since most of my documents are in English, multilingual support was not an important factor for this project.

---

## Grounded Generation

**System prompt grounding instruction:**  

The system prompt tells the LLM to answer questions using only the retrieved document chunks. If the retrieved documents do not contain enough information to answer the question, it is instructed to say that it does not have enough information instead of making up an answer. This helps keep the responses grounded in the documents instead of relying on the model's general knowledge.

**How source attribution is surfaced in the response:**  

After generating an answer, the system displays the names of the retrieved source documents below the response. This lets the user see which documents were used to answer the question and makes it easier to verify where the information came from.

---

## Evaluation Report


| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What courses are recommended during the first semester of the Queens College Computer Science BS program? | The recommended first-semester courses from the BS 4-Year Plan. | The system responded that it did not have enough information in the provided documents. | Partially Relevant | Inaccurate |
| 2 | How can a Computer Science student contact an academic advisor? | Advisor contact information, office location, email, phone number, and office hours. | The system retrieved the advising document and provided advisor contact information with source attribution. | Relevant | Accurate |
| 3 | What topics are covered in CSCI 313 – Data Structures? | Topics such as stacks, queues, trees, graphs, hash tables, searching, sorting, and algorithm analysis. | The system retrieved the undergraduate course document and correctly summarized the topics covered in CSCI 313 with source attribution. | Relevant | Accurate |
| 4 | What tutoring and academic support resources are available for Computer Science students? | Learning Commons tutoring, CSCI review sessions, Python workshops, LeetCode workshops, and other Computer Science support resources. | The system retrieved the tutoring resources and student resources documents and summarized the available academic support services with source attribution. | Relevant | Accurate |
| 5 | What opportunities does the AI Skill Foundry 3-Hour Micro-Internship provide for students? | Application process, Responsible AI training, live micro-internship experience, portfolio project, AI competency development, and possible stipend. | The system retrieved the AI Skill Foundry document and summarized the application process, internship experience, and program benefits with source attribution. | Relevant | Accurate |

**Retrieval quality:**  
- **Relevant:** The retrieved documents contained the information needed to answer the question.
- **Partially Relevant:** Related documents were retrieved, but they did not contain or surface the specific information needed.

**Response accuracy:**  
- **Accurate:** The response correctly reflected the retrieved documents.
- **Inaccurate:** The response did not correctly answer the question.
---

## Failure Case Analysis

**Question that failed:**

What courses are recommended during the first semester of the Queens College Computer Science BS program?

**What the system returned:**

The system responded, "I don't have enough information in the provided documents."

**Root cause (tied to a specific pipeline stage):**

The relevant document was included in the knowledge base, but the retrieval stage did not return the chunk containing the first-semester course recommendations. As a result, the language model did not receive the necessary context and correctly refused to generate an answer instead of making one up.

**What you would change to fix it:**

I would experiment with a larger chunk size, retrieve more chunks by increasing the top-k value, or reorganize the BS 4-Year Plan document so semester information stays together in a single chunk. This would make it easier for the retrieval system to find the correct information.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The planning document helped me organize the project before I started coding. It made me think about what documents to collect, how to split them into chunks, and what questions I wanted my system to answer. Having everything planned first made it easier to build each milestone step by step instead of trying to figure everything out while coding.

**One way your implementation diverged from the spec, and why:**

One thing I changed during implementation was the chunking strategy. I originally planned to use 500-character chunks with a 100-character overlap, but after testing I changed it to 400-character chunks with an 80-character overlap because my documents were relatively short. This produced more focused chunks and improved retrieval for most of my test questions, although one question still failed, showing there is room for improvement.
---

## AI Usage

**Instance 1**

* **What I gave the AI:**
I mainly used ChatGPT when I got stuck or wasn't sure how to move forward. I shared error messages, code snippets, or asked questions about how to implement the next part of the RAG pipeline.

* **What it produced:**
ChatGPT helped me debug errors, explained why certain issues were happening, suggested different approaches, and provided example code to help me move forward when I was stuck.

* **What I changed or overrode:**
I tested the suggested solutions, modified the code to fit my project, adjusted the chunking strategy, fixed dependency issues, and refined the implementation until it worked correctly with my own documents.

---

**Instance 2**

* **What I gave the AI:**
I used Claude for help implementing parts of the ingestion and chunking pipeline after I had already planned the project structure.

* **What it produced:**
Claude generated starter code for loading documents and splitting them into chunks, which gave me a good starting point for the implementation.

* **What I changed or overrode:**
I reviewed the generated code, adjusted the chunk size and overlap to better fit my documents, verified the chunk output, fixed issues during testing, and made additional changes so the implementation matched my final design and project requirements.
