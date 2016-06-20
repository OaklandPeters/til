Bash Shell: Writing command output to a file
===============================================

To capture all of a Bash command's output to the shell, into a file instead, this works:

```:bash
MYCOMMAND > output.txt 2>&1
```

This will capture both stderr and stdout. Note, this will prevent any of the normal output the shell, but you can check the `output.txt` in the text editor of your choice to get the same result.

A very common use case is for logging unit-test results. For example:

```
python test.py > test-results.txt 2>&1
```

