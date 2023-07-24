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

# Docs and Help
For documentation on how to use this API, refer to the Wiki.
Support is currently available through community forums only.


# License
This repository is licensed under the StarlightX Public License only.
To learn more, visit https://starlightx.io/licenses.

Basically, you are free to use, distribute, anything you want with it
as long as it is a consumer app and not a business app. In fact, we do
not even have the abilty to revoke your rights to it as long as you stay
in the Business2consumer segment. To use this product in
a business app, we will add a GPL license to it sometime early 2023.

We do not offer custom enterprise licenses, as the SXPL was made as
an alternative license to creative works such as games, without needing to
disclose source.


# Development
The project uses a FastAPI python backend, managed with PyTorch.
It can leverage any GPT4All compatible text-generation, and
will be compatible with OpenAI's GPT3.5 and GPT4.

# Performance
The CX Neural Engine runs fairly well on midrange hardware. For reference,
there is a ~26s inference time on a AMD Ryzen 5800H. We'll look into
GPU support when GPT4All supports GPU, although not many end users
will benefit from it as they'll probably need to virtualize the GPUs
to run in production.