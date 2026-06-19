# SSE
Backend half of SSE (there is also *[frontend part](../frontend/sse.md)*)

## Properties: SSE Backend Pieces
- HTMX SSE extension in /static/js/
- [ASGI](./asgi.md)
- Nginx config:
  ```nginxconf
  server {
    listen 80;
    location / {
        proxy_pass http://django:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_buffering off;
        proxy_cache off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
  }
  ``` 
- View:
  ```python
    import asyncio
    from django.http import StreamingHttpResponse
    from django.template.loader import render_to_string

    async def book_stream(request):
        """
        Asynchronously streams book updates as Server-Sent Events (SSE).
        """
        async def event_stream():
            while True:
                # 1. Fetch or generate updated data
                # (Use sync_to_async if querying the database)
                books = await get_latest_books_async() 
                
                # 2. Render a partial HTML template for the table rows
                html = render_to_string('partials/book_rows.html', {'books': books})
                
                # 3. Format the data for SSE (must start with 'data: ' and end with '\n\n')
                # HTMX will swap the content inside the 'data' field into your table
                yield f"data: {html}\n\n"
                
                # 4. Wait before the next update (e.g., 3 seconds)
                await asyncio.sleep(3)

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
  ```
- Url: `path('sse/', sse.book_stream, name='sse')`

## Workflow: How to add SSE to the app?
1. Make sure the project is ASGI-powered.
2. Make sure Nginx is configured for SSE
3. Write the view that returns `StreamingHttpResponse`
4. Make sure the view is in urlconfig

## Workflow: How to write the view that returns `StreamingHttpResponse`?
1. Copy the minimal example view above.
2. Rewrite it keeping 
    ```
    while True:
        ...
        await asyncio.sleep()
    ```