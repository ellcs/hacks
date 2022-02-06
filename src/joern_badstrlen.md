```
joern> var bad_strlen = ({cpg.method
         .name("(?i)strlen")
         .callIn
         .inAssignment
         .target
         .evalType("(g?)int")}).filter { c => c.lineNumber == Some(1385) }
```

# using `reachableBy` & `reachableByFlows`

```c
// $ cat test/test.c
#include <stdio.h>
#include <stdlib.h>

int getNumber() {
    int number = atoi("8");
    number = number + 10;
    return number;
}

void *scenario1(int x) {
    void *p = malloc(x);
    return p;
}

void *scenario2(int y) {
    int z = 10;
    void *p = malloc(y * z);
    return p;
}

void *scenario3() {
    int a = getNumber();
    void *p = malloc(a);
    return p;
}
```

```
~/bin/joern/joern-cli/joern
joern> importCode(inputPath = "test")
joern> run.ossdataflow
joern> def sink = cpg.method.callOut.name("malloc").argument
joern> def source = cpg.method.name("atoi").methodReturn
joern> sink.reachableBy(source).p
joern> sink.reachableByFlows(source).p
```
