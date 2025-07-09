from collections import Counter
import re

def tokenize(text):
    """Tokenizes text into words, removing punctuation and converting to lowercase."""
    return re.findall(r'\b\w+\b', text.lower())

def calculate_f1_score(original_text, summarized_text):
    """Calculates Precision, Recall, and F1-score for summarization accuracy."""
    original_tokens = tokenize(original_text)
    summary_tokens = tokenize(summarized_text)
    
    original_counter = Counter(original_tokens)
    summary_counter = Counter(summary_tokens)

    matching_words = sum((original_counter & summary_counter).values())
    
    precision = matching_words / len(summary_tokens) if summary_tokens else 0
    recall = matching_words / len(original_tokens) if original_tokens else 0
    
    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)
    
    return round(f1_score * 100 , 2)  # Convert to percentage

# Input and output texts
original_text = """Java is a high-level, object-oriented programming language developed by Sun Microsystems and released in 1995. It was designed to be platform-independent, meaning Java applications can run on different operating systems without modification. This is achieved through the Java Virtual Machine (JVM), which translates Java code into machine code at runtime. As a result, Java follows the principle of "Write Once, Run Anywhere" (WORA), making it highly portable and flexible. One of Java’s core strengths is its adherence to object-oriented programming (OOP) principles. It supports encapsulation, inheritance, and polymorphism, which help in structuring code efficiently, improving maintainability, and promoting reusability. This makes Java ideal for large-scale enterprise applications, where code organization and management are crucial. Additionally, Java has strong memory management, automatic garbage collection, and built-in exception handling, ensuring that applications remain stable and efficient.

Java is also renowned for its security features. It includes bytecode verification, class loading security, and runtime security checks to prevent unauthorized access and vulnerabilities. This makes Java a preferred choice for banking, financial, and enterprise applications, where security is paramount. Another reason for Java's widespread adoption is its vast ecosystem of frameworks and libraries, such as Spring for enterprise applications, Hibernate for database management, and JavaFX for graphical user interfaces. Java is also the foundation of Android app development, making it one of the most commonly used languages for mobile applications.

Despite being a robust language, Java remains beginner-friendly due to its simple syntax and comprehensive documentation. With a rich API and strong community support, Java developers can easily access resources, tutorials, and libraries to build efficient applications. Whether used for web applications, mobile development, cloud computing, or data analysis, Java remains a fundamental language in the software industry.

Java follows the object-oriented paradigm, which means applications are designed around objects that interact with each other. This makes it easier to develop, debug, and scale software. Encapsulation allows data hiding, inheritance enables code reuse, and polymorphism provides flexibility in code execution. These features make Java a structured and maintainable language.

Java’s popularity is also due to its cross-platform compatibility, achieved through the JVM. The JVM acts as a bridge between Java code and the underlying hardware, ensuring that Java programs can run on Windows, Linux, macOS, and other platforms without modification. This is why Java is widely used in enterprise environments, where software must work across multiple systems.

Java also provides automatic memory management through garbage collection, which removes unused objects from memory. This prevents memory leaks and ensures that applications run smoothly without excessive memory consumption. Furthermore, Java’s exception handling mechanism makes it easier to detect and fix errors, improving software reliability.

Overall, Java is a powerful, secure, and versatile programming language. Its object-oriented approach, platform independence, memory management, and security features make it an excellent choice for developers in various domains, including web development, mobile apps, enterprise solutions, and cloud computing."""

summarized_text_25 = """This makes Java ideal for large-scale enterprise applications, where code organization and management are crucial.
Additionally, Java has strong memory management, automatic garbage collection, and built-in exception handling, ensuring that applications remain stable and efficient.
This makes Java a preferred choice for banking, financial, and enterprise applications, where security is paramount.
Java is also the foundation of Android app development, making it one of the most commonly used languages for mobile applications.
Whether used for web applications, mobile development, cloud computing, or data analysis, Java remains a fundamental language in the software industry.
These features make Java a structured and maintainable language.
Its object-oriented approach, platform independence, memory management, and security features make it an excellent choice for developers in various domains, including web development, mobile apps, enterprise solutions, and cloud computing."""

summarized_text_50 = """Java is a high-level, object-oriented programming language developed by Sun Microsystems and released in 1995.
It was designed to be platform-independent, meaning Java applications can run on different operating systems without modification.
As a result, Java follows the principle of "Write Once, Run Anywhere" (WORA), making it highly portable and flexible.
This makes Java ideal for large-scale enterprise applications, where code organization and management are crucial.
Additionally, Java has strong memory management, automatic garbage collection, and built-in exception handling, ensuring that applications remain stable and efficient.
This makes Java a preferred choice for banking, financial, and enterprise applications, where security is paramount.
Java is also the foundation of Android app development, making it one of the most commonly used languages for mobile applications.
With a rich API and strong community support, Java developers can easily access resources, tutorials, and libraries to build efficient applications.
Whether used for web applications, mobile development, cloud computing, or data analysis, Java remains a fundamental language in the software industry.
Java follows the object-oriented paradigm, which means applications are designed around objects that interact with each other.
These features make Java a structured and maintainable language.
The JVM acts as a bridge between Java code and the underlying hardware, ensuring that Java programs can run on Windows, Linux, macOS, and other platforms without modification.
Overall, Java is a powerful, secure, and versatile programming language.
Its object-oriented approach, platform independence, memory management, and security features make it an excellent choice for developers in various domains, including web development, mobile apps, enterprise solutions, and cloud computing."""

summarized_text_75 = """Java is a high-level, object-oriented programming language developed by Sun Microsystems and released in 1995.
It was designed to be platform-independent, meaning Java applications can run on different operating systems without modification.
This is achieved through the Java Virtual Machine (JVM), which translates Java code into machine code at runtime.
As a result, Java follows the principle of "Write Once, Run Anywhere" (WORA), making it highly portable and flexible.
One of Java’s core strengths is its adherence to object-oriented programming (OOP) principles.
This makes Java ideal for large-scale enterprise applications, where code organization and management are crucial.
Additionally, Java has strong memory management, automatic garbage collection, and built-in exception handling, ensuring that applications remain stable and efficient.
Java is also renowned for its security features.
This makes Java a preferred choice for banking, financial, and enterprise applications, where security is paramount.
Another reason for Java's widespread adoption is its vast ecosystem of frameworks and libraries, such as Spring for enterprise applications, Hibernate for database management, and JavaFX for graphical user interfaces.
Java is also the foundation of Android app development, making it one of the most commonly used languages for mobile applications.
With a rich API and strong community support, Java developers can easily access resources, tutorials, and libraries to build efficient applications.
Whether used for web applications, mobile development, cloud computing, or data analysis, Java remains a fundamental language in the software industry.
Java follows the object-oriented paradigm, which means applications are designed around objects that interact with each other.
These features make Java a structured and maintainable language.
The JVM acts as a bridge between Java code and the underlying hardware, ensuring that Java programs can run on Windows, Linux, macOS, and other platforms without modification.
This is why Java is widely used in enterprise environments, where software must work across multiple systems.
Java also provides automatic memory management through garbage collection, which removes unused objects from memory.
Furthermore, Java’s exception handling mechanism makes it easier to detect and fix errors, improving software reliability.
Overall, Java is a powerful, secure, and versatile programming language.
Its object-oriented approach, platform independence, memory management, and security features make it an excellent choice for developers in various domains, including web development, mobile apps, enterprise solutions, and cloud computing."""

# Calculate F1-score
f1_score = calculate_f1_score(original_text, summarized_text_75)
f1_score
print("Accuracy score (25%): ", (len(original_text) / (len(summarized_text_25)/0.25)*100))
print("Accuracy score (50%): ", (len(original_text) / (len(summarized_text_50)/0.5)*100))
print("Accuracy score (75%): ", (len(original_text) / (len(summarized_text_75)/0.75)*100))