# Generative Software: Just-in-Time Software from a Series of Prompts

Software reduced the marginal cost of replicating an idea to zero. The internet reduced the marginal cost of distributing media to zero. Stacked together, software distribution over the internet resulted in the technology boom of the past 30 years. However, the total cost of producing, operating, and evolving software has increased over time—primarily due to the shortage of software engineering talent and the poor adoption of effective engineering practices.

Generative AI, with its ability to translate product specifications into working software, has the potential to do for software production and evolution what software and the internet did for replication and distribution.

In the near future, it will be feasible to turn a product specification into a sequence of prompts, which can then be used to generate software on demand. Let’s call this type of software generative software, and the sequence of prompts used to produce it a generative specification (or generative spec).

In contrast to the current software distribution model, where the software itself is the distributed asset, the generative software model distributes the generative specification. This is analogous to Just-in-Time Compilation, where bytecode in languages like Java is transformed into machine code on demand to optimize execution.

## Examples

In keeping with the longstanding tradition of programming examples, here is a simple generative spec:
```
A program that outputs “Hello, World!” when executed from the command line.
```
A slightly more complex example to illustrate a generative specification where each prompt yields a verifiable, testable, or reusable component:
```
Product Specification: Create a command-line tool named wordcount that outputs
the number of lines, words, and characters in a file.

Generative Specification:
    1. Write a function that takes a string as input and returns the number of
       lines, words, and characters.
    2. Write a function that reads the contents of a file given its file path
       and returns it as a string.
    3. Write a command-line wrapper that uses both the file reader and the
       analysis function, and prints the results in aligned columns.
    4. Add error handling for missing or unreadable files, and print helpful
       error messages.
    5. Write two usage examples of this tool being run from the terminal,
       including expected output.

```
To make generative software more useful, we need the following attributes:
  -	The generative specification should be written in human language.
  -	It should be evolvable by both humans and AI.
  -	The resulting generative software should be consistent with the product specification.
  -	It should be reproducible—and therefore, by design, disposable.

## Frequently Answered Questions

1. How is this different from current coding assistants?
Current coding assistants produce software, and we distribute that software. In contrast, this model operates at a higher level of abstraction: we distribute the sequence of prompts that produced the software. It remains unclear how to convert the chat history of current coding assistants into a structured generative spec.

2. What are the benefits of generative software?
	- It may be approachable to more people—not just software engineers.
	- Implementers can choose the tech stack (within reasonable constraints).
	- Much of the accumulated [technical debt](https://github.com/kulesh/dotfiles/blob/master/dev/dev/docs/a-field-guide-to-technical-debt.md) can be addressed through regeneration.
	- …

3. What makes each prompt in the generative spec a unit?
Each prompt expresses a clear intent that yields a verifiable, testable, or reusable component of the generative software.

4. What’s next?
	- Develop a working example of slightly more complex software than “Hello, World!” (e.g., a generative blog engine).
	- Design a sensible format for prompt sequencing.
	- Build tooling to convert product specs into generative specs.
	- Explore how to represent more complex software with integrations and dependencies.
	- …
