# Experience Summary

This activity showed how AI can speed up the early stages of a programming project, especially when turning requirements into a project structure. The AI helped identify the main components of the Personal Note-Taking System: a PyQt user interface, a note data model, local storage, image attachment handling, filtering, documentation, and tests.

The most useful part of the AI assistance was breaking the assignment into smaller implementation decisions. Instead of placing all logic directly in the GUI, the project separates note storage into `pnts/storage.py` and the interface into `pnts/app.py`. This made the code easier to test and easier to understand.

I still had to evaluate the AI-generated choices. JSON storage is appropriate for this assignment because it is simple and transparent, but it would not be the best choice for a large multi-user system. Copying image attachments into the app's own data folder is safer than storing only the original file locations, but it also means the app uses extra disk space. The application meets the required features, but future improvements could include editing existing notes, exporting notes, and better image thumbnail controls.

The later bug-fix pass also showed why generated code should be tested visually and behaviorally. The first version worked at a basic level, but review found better ways to handle corrupt saved data, unsupported attachments, and unclear UI states. The improved version is more reliable because it validates inputs and gives the user clearer feedback.

Overall, the experience demonstrated that AI is helpful as a development assistant, but the programmer still needs to check requirements, test behavior, inspect the interface, and understand the code before submitting it.
