# StarlightX Character Neural Engine
This is the StarlightX Neural Engine repository.

We bring the bleeding edge Machine Learning technologies (Llama2)
directly into gameplay!
## Run Server
To run from the server, there are scripts provided to run. 
Linux and MacOS users use the serve.sh, and Window users use the serve.bat.

For the inference server, run the inference-server.sh script, or if you already have,
just run the binary in the library using paramaters in the inference-server script.
Then, drop models into the Models folder.

Note: The binaries in the lib/ folder are compiled on and are for a Redhat >8 equivalent.

# Docs and Help
For documentation on how to use this API, refer to the Wiki.

## Basic API

To integrate with the server with an app, first send a GET to https://{url-of-backend}/genkey/

This returns a JSON response with 2 paramaters, a key and a session token.

The key is for tracking context of the model, and the session token is to prevent others from corrupting

other's context sessions. Once you have the tokens, send a POST to https://{url-of-backend}/ask/ with 

the following JSON data:


`character | string`

`message | string`

`chatID (the key) | number`

`session | string`

Then, you will recieve a JSON response with the following:

`response | string`

`emotion | [string1, string2, string3...]`

Now, you have a working interaction between the Character Neural Engine and your frontend!

## Support

Support is currently available through community forums only.
https://community.starlightx.io

# Limitations
The model response accuracy may not be as finetuned as we want. While between characters,
it talks pretty distiguisable, sometimes, it just straight up does a bad job, leaves it empty,
etc. We will attempt to fix this before our launch by finetunning the model we use, Llama V2.



The emotions portion of the AI engine is extremely inaccurate, due to a feed through to 
Llama instead of a dedicated AI. We expect this to be patched relatively soon.
the model talk with generic "chatbot" like tones. 
# License
This repository is licensed under the StarlightX Public License only.
To learn more, visit https://starlightx.io/licenses.

Basically, you are free to use, distribute, anything you want with it
as long as it is a consumer app and not a business app. While not Open Sourced,
we do not have the abilty to revoke your rights to it as long as you stay
in the Business -> Consumer segment. To use this product in
a business app, we will add a GPL license to it sometime early 2024.

We do not offer custom enterprise licenses, as the SXPL was made as
an alternative license to creative works such as games, without needing to
disclose source.


# Development
The project uses a FastAPI python backend, managed with Poetry.
It is compatible with llama.cpp server, and
will be compatible with OpenAI's GPT3.5 and GPT4.

Note: Do not commit **any** Facebook Llama weights into this repository, or display links
to Llama weights anywhere in this repository for any reason. To get the official Llama 
weights, get them from [Facebook](https://ai.meta.com).

# Performance
We are currently working on the performance of the model, and finetuning the prompts. We
are also looking into finetuning Llama 2 to support personalization more.
## Hardware Performance

The inference server runs fairly well on midrange hardware. For reference,
there is a ~26s inference time on a AMD Ryzen 5800H.

All of the below is at n_threads = physical cores. Time per response are a 3 sample average.

|CPU |Model  | Time per Response|
--- | --- | ---|
|AMD Ryzen 7 5800H | Llama v2 13B | 30.169s|
|Xeon E5 2670 (4 Core VM)| Llama v2 13B | 89.36s|
|AMD Ryzen 7 5800H + 4 layers to NVIDIA RTX 3050 Ti | Llama v2 13B | 18.864s|
|Intel i7 13700K + 15 layers to NVIDIA RTX 4070 | Llama v2 13B |2.171s |

## Future Optimizations

We are looking to swap out the emotions AI to a dedicated text -> emotions AI. 
This will bring significant performance in both the AI model and the hardware,
as they are no longer wrapped to such a large model.

For the game [Light the World](https://ltw.starlightx.io), we'll likely bake the FastAPi
into a C++ file and then deploy to Unreal Engine as a binary.
