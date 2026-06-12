```python
class Developer:
    total_developers = 0

    def __init__(self, name, age, occupation, skills):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.skills = skills
        self.projects = []
        self.active = True

        Developer.total_developers += 1

    def add_project(self, project):
        if not isinstance(project, str):
            raise TypeError("Project name must be a string.")

        self.projects.append(project)

    def introduce(self):
        return (
            f"Hi, I'm {self.name}.\n"
            f"{self.age} years old | {self.occupation}\n"
            f"Skills: {', '.join(self.skills)}"
        )

    def build(self):
        if not self.projects:
            return "Currently building new ideas..."

        return f"Working on: {', '.join(self.projects)}"

    @property
    def experience_level(self):
        if len(self.skills) >= 8:
            return "Advanced"
        elif len(self.skills) >= 4:
            return "Intermediate"
        return "Beginner"

    @staticmethod
    def mindset():
        return "Learn • Build • Break • Fix • Repeat"


dev = Developer(
    name="Arshad Moerat",
    age=41,
    occupation="Full Stack Software Developer",
    skills=[
        "Python",
        "FastAPI",
        "PostgreSQL",
        "NextJS",
        "React",
        "MySQL",
        "Typescript",
        "Sentence Transformers",
        "Ollama",
        "LLMs",
        "Qdrant",
        "Vector DBs",
        "REST APIs",
        "RAG Systems"
    ]
)

try:
    dev.add_project("MagnaFlow-Lite")
    dev.add_project("FieldSync")
    dev.add_project("RepoScribe-RAG")
    dev.add_project("LocalDesk-AI")
    dev.add_project("StockPilot")
    dev.add_project("FlowForge-AI")

except Exception as e:
    print(f"Error: {e}")

print(dev.introduce())
print(dev.build())
print(f"Experience Level: {dev.experience_level}")
print(f"Mindset: {Developer.mindset()}")
print(f"Developers Created: {Developer.total_developers}")
```

## Output

```text
Hi, I'm Arshad Moerat.
41 years old | Full Stack Software Developer
Skills: Python, FastAPI, PostgreSQL, NextJS, React, MySQL, Typescript,
Sentence Transformers, Ollama, LLMs, Qdrant, Vector DBs, REST APIs, RAG Systems

Working on: MagnaFlow-Lite, FieldSync, RepoScribe-RAG,
LocalDesk-AI, StockPilot, FlowForge-AI

Experience Level: Advanced
Mindset: Learn • Build • Break • Fix • Repeat
Developers Created: 1
```
