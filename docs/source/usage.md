# Workflow: Dpgstack
**1. Create a model.**
2. Run `just suit_model Book books table`.
3. See the data in browser.
4. Decide what you want to do with that data next?
**5. Invoke `/add_view_action` workflow in Cline. It will edit model's template and view to achieve desired functionality**
*Repeat steps 4-5 until satisfied with the web app*
6. Edit tailwind classes in templates to make sure the app satisfies the styling look.
**7. Invoke `/deploy example.com prod` workflow**
*8. Repeat steps 1-6. Then run `git push`.*

The workflow:
1. Define the data.
   1. Create Model class
   2. Run `just suit {{Model}} {{app}} {{layout}}`, where:
    - {{Model}}: Model class: `Book`
    - {{app}}: App name, located in ./apps: `books`
    - {{layout}}: A way to display data:
      - `cards`
      - `table`
   3. *Everything model needs is generated*. Run tests to make sure.
   4. Start debug server, go over `http://localhost:8000/{{app}}/{{model}}/`, see the data displayed.
2. Define the behavior of that data in the view.
3. Create view action and send htmx request from template there.


*As long as views are stable and tested, you can stretch any kind of twisted AI generated garbage templates on them. Just make sure to split templates into components, so its easier to churn it into AI.*