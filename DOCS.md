Cinnamon Gum is a text-processing golfing language. 

One of the first things to note is that all CG programs are compressed. There are three supported compression schemes:

- DEFLATE (I recommend `zopfli` for optimal compression)
- LZMA (using raw format)
- Base conversion (more precisely, treating the code as a base 96 number and converting it to base 256)

CG will (usually) automatically detect which compression scheme was used. The included `cinnamon-compressor` (needs `zopfli` and `lzma`) will automate the compression for you by trying each compression scheme and outputting the shortest result. It will also handle setting the first byte to the first stage mode: the examples here will use the format you would pass to `cinnamon-compressor`. Make sure you don't have any trailing newlines when you compress your code; the compressor won't strip those out.

# Modes

Cinnamon Gum programs consist of various *stages*, each with a *mode*. The mode of the first stage is specified by the leading byte of the compressed string; the other stages are constructed by "outputting" a string with a backtick followed by the desired mode. There are two kinds of modes:

- Execute modes. These modes fully consume the code and either output a string or execute another stage (indicated by outputting a leading backtick followed by the next stage's code).

- Modify modes. These modes modify the code or input in some way, then remove themselves from the code and execute the remaining code.

Here's an (uncompressed) example:

    l0&Just a zero;1&`dA`fHi %s

Let's deconstruct it:

The first mode is the execute mode `l`, or *l*ookup mode. It parses the code in the format of:

    key1&key2&...&value;...

and then maps input to the appropriate value. In the case of an input of `0`, the result is the string `Just a zero`, which CG simply prints to STDOUT. In the case of `1`, however, the resulting string is `` `dABC`fHi %s``. CG sees the backtick and treats this as a new stage.

This next stage's mode is the modify mode `d`, which takes the next line of input and removes anything matching the specified regex: in this case it simply deletes any uppercase `A`s. The result is then passed as input to the next stage. This stage has the execute mode `f`, or print*f*. In this case, it simply substitutes the `%s` with our result from the last stage.

So, for a sample input `1\n"Abc"` (note the double quotes, that's required for string input in most cases), the result would be `Hi bc`.

Here is a list of all modes:

  **Coming soon**

# Input handling

In most cases, when a stage needs input it either takes the next line of input from STDIN or the last line of input received if STDIN is exhausted. However, as we saw with `d`, modify modes that modify input can then pass that input on to the next stage. Additionally, you can also explictly give input to a stage using `!`. Anything after an `!` in a stage's code is passed as input to that stage.

Here's a rudimentary example:

    `fHello, %s here!Cinnamon Gum`

This passes the input string `Cinnamon Gum` to the `f` stage. Do note that a stage will only read `!` input or input from a modify mode if STDIN is already exhausted; this limitation will probably be removed in the future.

# Sample programs

**Coming soon**
