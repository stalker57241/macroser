# Macroser
[![Upload Python Package](https://github.com/stalker57241/macroser/actions/workflows/python-publish-testpypi.yml/badge.svg?branch=general&event=milestone)](https://github.com/stalker57241/macroser/actions/workflows/python-publish-testpypi.yml)

Program to unwrap special macros

# Build

Install `build`:
```sh
$ python -m pip install --upgrade build
```
Build it
```sh
# To build:
$ python -m build .
# To install:
$ python -m pip install .
```

# How to run

```sh
$ python -m macroser -Imacros -M@ file.in
```
## -I\<folderpath\>

To include folder

## -o\<filename\>

To specify filename

## -M\<prefix\>

To specify used prefix.
It can be a string (Like "@@", or "_@"). Maybe you can refactor code using it (Not tested, but sounds interesting... `python -m macroser -Mvec2i_ file.in`)

# Header syntax

This lib allows to recursive macrosing
```C
macros/macro
Everything out of defines is comment
define VECTOR(name, type, fields...)
  typedef struct { @type @fields; } @name;
enddefine
define VECTOR_ADD_FIELD(field)
  .@field = a.@field + b.@field
enddefine
define VECTOR_ADD(name, field...)
  @name @name_add(@name a, @name b) {
    return (@name) {
      @(foreach VECTOR_ADD_FIELD, @field)
    };
  }
enddefine
define FIRST_EXISTS(a, b)
  @(optional a,b)
enddefine
```
# Source syntax
```C
// main.c.in
#include <stdio.h>
@(include macro) // Macroser understands when include is absolute.
@(VECTOR vec3i, int, x, y, z)
@(VECTOR_ADD vec3i, x, y, z)

int main() {
  vec3i a = {
    .x = 1,
    .y = 3,
    .z = 0
  };
  vec3i b = {
    .x = 1,
    .y = 3,
    .z = 0
  };
  vec3i c = vec3i_add(a, b);
  printf(" A+B=C");
  printf("x%d %d %d", a.x, b.x, c.x);
  printf("y%d %d %d", a.y, b.y, c.y);
  printf("z%d %d %d", a.z, b.z, c.z);
  return 0;
}
```
Built with `python -m macroser -Imacros main.c.in`:
```C
// main.c

#include <stdio.h>
// Macroser understands when include is absolute.
typedef struct { int x, y, z; } vec3i;
vec3i vec3i_add(vec3i a, vec3i b) {
return (vec3i) {
.x = a.x + b.x,
.y = a.y + b.y,
.z = a.z + b.z
};
}

int main() {
  vec3i a = {
    .x = 1,
    .y = 3,
    .z = 0
  };
  vec3i b = {
    .x = 1,
    .y = 3,
    .z = 0
  };
  vec3i c = vec3i_add(a, b);
  printf(" A+B=C\n");
  printf("x%d %d %d\n", a.x, b.x, c.x);
  printf("y%d %d %d\n", a.y, b.y, c.y);
  printf("z%d %d %d\n", a.z, b.z, c.z);
  return 0;
}
```
