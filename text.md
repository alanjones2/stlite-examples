# stlite: Serverless Streamlit
## stlite is a browser-based implementation of Streamlit that can run apps on a web page without having to deploy to a Streamlit server

![](https://github.com/alanjones2/stlite-examples/blob/main/0_4aM0SBn1NeWpOCMX.jpg?raw=true)

Are you being served? - Photo by Blake Wisz on Unsplash

Of course, there is always a server involved. A simple web page is loaded from a server (along with its dependencies) before being displayed in the browser. 

By 'serverless' we mean that there is no server-based code that is an integral part of the web application. In a typical server-based application, such as a Flask app, the web page - typically as a result of a user action - will call a function on the server to retrieve new data and the web page will be updated with this data.

Streamlit is very much server-based: each time there is a user interaction the server is notified, the whole of the application is re-run on the server, and the web page is updated.

A Streamlit app is coded in Python so the server requires a Python interpreter along with the Streamlit library to run the app and generate the web page.

### Pyodide
So, how can we operate without a server where the Python code runs? 

Answer: Pyodide. 

Pyodide is a Python interpreter that has been ported to Web Assembly (WASM) and so can run in a browser. 

Being able to natively run Python in the browser is quite a thing; it means that we can run code that uses, for example, data science libraries that provide functionality that is not available in Javascript. And, on the other hand, because Pyodide provides communication with Javascript, the Python code can use Javascript libraries whose functionality is not available in Python (e.g. web graphics).

### stlite
stlite is a port of the Streamlit library to WASM and combines with Pyodide to create a method of running Streamlit apps directly in the browser.

Why is that good?

Well, it means you can deploy Streamlit apps to any website and not have to rely on Streamlit Cloud or alternative hosting sites. Also, can use whatever deployment method suits you, you don't necessarily have to use GitHub - which may or may not appeal to you.

One thing that may not appeal to you is, that because everything resides in the web browser, it is potentially public: this means that you should not include anything secret in your app (such as API keys).
But bearing these things in mind, let's see how we can create Streamlit apps in the browser.

### Hello stlite
A stlite app is fundamentally  an HTML page with embedded Python. You don't need to know HTML, though: the small amount that you need is boilerplate code that you can reuse for each app.

Below is the first app that appears on the _stlite_ web page (reproduced here under the Apache2 license).

```python
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>stlite app</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css"
    />
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
    <script>
      stlite.mount(
'
import streamlit as st

name = st.text_input('Your name')
st.write("Hello,", name or "world")
',
        document.getElementById("root")
      );
    </script>
  </body>
</html>

```

It's a 'hello world' program that prompts for a name and says 'Hello' to that name or 'Hello world' if no name has been entered. 

The Streamlit code is enclosed in quotes and inside the call to the function `stlite.mount`. This function is from the Javascript library that was loaded earlier in the listing (as was the stlite css file) and it runs the Streamlit code inside the HTML element specified in it's second parameter, i.e. `document.getElementById("root")`.

Load this page in your browser and you will see the following.

![](https://github.com/alanjones2/stlite-examples/blob/main/stlite-examples/Screenshot-hello.png?raw=true)

It's the same as you would get by running the Streamlit code as a separate app. The only difference is the startup time: a _stlite_ web page has to load and execute the Javascript library which is a fairly lengthy process, so you will see various messages flashed up on the screen while the app is loading. This delay occurs only once; afterwards the app has loaded it is quick to run.

This first _stlite_ app can be run directly in the browser (e.g. by double-clicking it in the file explorer). However, the next programs that we will encounter will consist of more than one page and so, in order to avoid CORS errors, we need to run then in a local server. So, navigate to the folder where you store the files and run the command:

```bash
python -m http.server
```

Depending on your set up, you may need to use `python3` instead of `python`.

this command will start a local server and if you open `localhost:8000`in your browser you will see a list of the files that you can run in the browser.

### Separate files

I'm not keen on mixing different languages in the same file and luckily _stlite_ allows us to separate the python files from the main HTML. We do this by specifying the file path in the `stlite.mount()`function instead of the actual code. The call to mount will look something like this:

```javascript
    stlite.mount(
      {
        entrypoint: "hello.py",
        files: {
          "hello.py": {
            url: "hello.py",
          },
        },
      }
```

Instead of a simple string containing the code the we specify a dictionary. The first entry in the dictionary is the file which will be the starting point for the app (yes, you can have more than one file!). The second entry specifies the file names and the url of the file (these are not the same, the `entrypoint` is the name in the virtual file system that Pyodide uses; `url` refers to the path to the original file in _your_ file system.)

So, in this code we are telling _stlite_ to copy the file "hello.py" is your local file system into a file of the same name in the local file system. And previous to that we specified a file virtual file system as the starting point for the app.

The full code for the HTML file is shown below. As you will see it is pretty similar to the first program except for the changes detailed above.


```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>stlite app</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css" />
</head>

<body>
  <div id="root"></div>
  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
  <script>
    stlite.mount(
      {
        entrypoint: "hello.py", // The target file of the `streamlit run` command
        files: {
          "hello.py": {
            url: "hello.py",
          },
        },
      },
      document.getElementById("root")
    );
  </script>
</body>

</html>
```

Now we need to write the actual Python code in "hello.py".

```python
import streamlit as st

st.markdown("# :balloon: Hello from :red[stlite] :balloon:")
```
Now when we run the HTML in the browser we wil see this:

![](https://github.com/alanjones2/stlite-examples/blob/main/Screenshot-hello-red.png?raw=true)

### Multiple files and libraries

Streamlit supports multiple pages and so does _stlite_. We simply need to add extra file specs to the dictionary passed to `stlite.mount` - you see the idea in the code below.

```javascript
    stlite.mount(
      {
        requirements: ["matplotlib"],
        entrypoint: "hello.py", // The target file of the `streamlit run` command
        files: {
          "hello.py": {
            url: "hello.py",
          },
          "pages/histogram.py":{
            url: "histogram.py"
          }
        },
      },
      document.getElementById("root")
    );
```

Here the dictionary now contains to entries, the original "hello.py" and a new file that is located in the _pages_ folder called _histogram.py_. (You probably already know that the _pages_ folder is where Streamlit expects to find the files for a multi-page app.)

The additional file draws a histogram from a set of random numbers, so we need to import the _matplotlib_ library to draw the chart. In addition to the Python `import`, we also need to tell Pyodide which libraries we are going to use. This is done in an additional dictionary entry:

```python
requirements: ["matplotlib"]
```

Here is the full HTML code for the multi-page app.

```html
<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>stlite app</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css" />
</head>

<body>
  <div id="root"></div>
  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
  <script>
    stlite.mount(
      {
        requirements: ["matplotlib"],
        entrypoint: "hello.py", // The target file of the `streamlit run` command
        files: {
          "hello.py": {
            url: "hello.py",
          },
          "pages/histogram.py":{
            url: "histogram.py"
          }
        },
      },
      document.getElementById("root")
    );
  </script>
</body>

</html>
```

And here is the new Python code that is in the file _pages/histogram.py_

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

size = st.slider("Sample size", 100, 1000)

arr = np.random.normal(1, 1, size=size)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
```

The combination of these file produces a typical Streamlit multi-page application with the navigation in the sidebar.

![histogram](https://github.com/alanjones2/stlite-examples/blob/main/Screenshot-pages.png?raw=true)

### Conclusion

That a brief run through of _stlite_ and I hope you have found it useful.

_stlite_ provides us with a fairly simple way of producing serverless Streamlit app that can be uploaded as static pages to, for example, GitHub Pages, or any other static HTML file server. It support mult-page applications and let's us load libraries such as _matplotlib_.

You can find more details in the _stlite_ GitHub repository (see Notes below) and you can find the source code for this article in my GitHub repository, [here](https://github.com/alanjones2/stlite-examples).

Thanks for reading!

### Notes

1. The _stlite_ GiHub repository is [here](https://github.com/whitphx/stlite)

2. Some of the code in this article is derived or copied from _stlite_ in accordance with the [Apache2 license](https://www.apache.org/licenses/LICENSE-2.0).

3. All images/screenshots are by me, the author, unless otherwise noted.

4. You can find more articles on Medium or via my [website](https://alanjones2.github.io) and you can subscribe to my occasional newsletter, [here](https://technofile.substack.com).
