# Custom Database in C

This is my walkthrough of the db_tutorial found [here](https://cstack.github.io/db_tutorial/)
The code seen in this tutorial was hand-typed by myself while reading through the
tutorial. I decided to write my own tests, using python's unittest, because the
author uses *rspec* which I'm not entirely familiar with, so I decided to write
my own tests.

## Notes to self

### Compiler

It looks like the tutorial may be using the *clang* compiler. There were too many
issues in my attempts to use *gcc*.

The code that wouldn't work with *gcc* was:

```c
const uint32_t COLUMN_USERNAME_SIZE = 32;
const uint32_t COLUMN_EMAIL_SIZE = 255;
struct Row_t {
    uint32_t id;
    char username[COLUMN_USERNAME_SIZE];
    char email[COLUMN_EMAIL_SIZE];
};
```

This bit fails with the *gcc* compiler with the following errors:

    error: variably modified 'username' at file scope

This error is happening because *gcc* doesn't treat *const* in the same way that
*clang* does. The fix here is to use *#define* statements instead of *const uint32_t*
which would have to be used for _every_ single *const* statement in this code.

I'll just stick with *clang* for now.