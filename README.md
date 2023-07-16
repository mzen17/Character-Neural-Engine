# StarlightX Character Demo API
This is the backend for the StarlightX Neural Engine.

To make requests, use this format:

`https://{url-of-backend}/return`

with a JSON post with 
{ChatID (String), Message (String)}.

This API will return it will a JSON of

{
    returnVal: [value1, value2, value3]
    emotions: [value1, value2, value3...]
}

## Run Server
To run from the repo (good for nonproduction use), run the serve file in the run. 
Linux and MacOS users use the serve.sh, and Window users use the serve.bat.

For production, it is highly recommended to use Docker to run the backend.