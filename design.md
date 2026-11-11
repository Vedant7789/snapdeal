 Design Document — AI Voice KAM

 1. Overview

AI Voice KAM (Key Account Manager) is an AI-powered conversational assistant designed to help e-commerce sellers understand their business performance through natural language conversations.

Instead of navigating multiple dashboards and manually interpreting metrics, sellers can ask questions about their business and receive contextual, conversational insights.

The system combines an LLM-powered conversational workflow with business analytics and voice interaction.

 2. Problem Statement

E-commerce sellers frequently need to investigate changes in important business metrics, including:

- Sales and revenue
- Order volume
- Cancellation rates
- Product performance

Traditional dashboards provide numerical information but often require sellers to manually interpret the data.

The goal was to build an assistant that makes business information accessible through natural language.

3. System Architecture

The application follows a modular architecture with separate responsibilities for conversation handling, LLM integration, analytics, and voice processing.

 High-level workflow

1. The user submits a question through the interface or voice input.
2. Speech input is converted into text when voice interaction is used.
3. The backend processes the query and maintains conversational context.
4. The LLM interprets the question and determines the appropriate response workflow.
5. The analytics service retrieves relevant business metrics.
6. The LLM generates a natural-language response using the available information.
7. The response is returned to the user.
 Architecture diagram

text
             User
               |
               v
       Voice / Text Input
               |
               v
       Speech Recognition
               |
               v
        Backend API
               |
               v
     Conversation Manager
               |
               v
          LLM Layer
               |
               v
       Analytics Service
               |
               v
       Business Metrics
               |
               v
      Contextual Response
               |
               v
          User Output


 4. Core Components

 A. Conversational AI

The conversational layer uses an LLM to understand natural-language questions and generate context-aware responses.

It supports follow-up questions and conversational interactions rather than relying exclusively on predefined question formats.

 B. Business Analytics

The analytics service processes business performance metrics and calculates changes between reporting periods.

For example:

- Current versus previous sales
- Current versus previous order volume
- Cancellation rate changes

The application uses these calculations to provide context for the LLM's responses.

 C. Voice Interaction

The voice workflow allows users to interact with the assistant through speech.

The system converts speech into text, processes the resulting query, and generates a conversational response.
 D. Backend API

The backend coordinates requests between the user interface, conversational layer, and analytics service.

The modular structure makes it easier to extend individual components without tightly coupling the entire application.

 5. Key Design Decisions

 Modular architecture

Different responsibilities are separated into individual modules. This improves maintainability and makes future extensions easier.

 Analytics before response generation

Business metrics are calculated by the analytics layer rather than relying on the LLM to perform every numerical calculation.

This helps improve numerical consistency and reduces the possibility of fabricated business figures.

 Natural-language interaction

The application prioritizes conversational interaction so that sellers can investigate business questions without needing to understand the underlying data structure.
 Separation of concerns

Voice processing, business analytics, conversation management, and LLM orchestration are treated as distinct responsibilities.
6. Example Interaction

User: Why have my sales dropped this month?

AI KAM: Your sales and orders have both decreased by 32.5% compared to the previous month. Have you noticed any changes in your product listings or pricing that might have affected sales?

The assistant uses available analytics to establish the context before generating a conversational explanation.

 7. Reliability and Limitations

The system is an independently developed prototype and is not production-ready.

Current limitations include:

- Business insights depend on the availability and quality of the underlying business data.
- LLM-generated explanations may require human verification.
- Voice recognition can be affected by audio quality and background noise.
- The current implementation is designed around e-commerce seller workflows.

The architecture can be extended with additional data sources, integrations, and capabilities.

## 8. Future Improvements

Potential improvements include:

- Persistent conversation memory across sessions.
- Integration with live e-commerce APIs.
- More advanced tool orchestration.
- Source-backed web research capabilities.
- Improved speech recognition and response latency.
- Evaluation pipelines for response accuracy and reliability.

## 9. Conclusion

AI Voice KAM explores how conversational AI can simplify business analytics and make actionable information more accessible to e-commerce sellers.

The project demonstrates the integration of LLMs, backend services, business analytics, and voice interaction into a modular AI application.
