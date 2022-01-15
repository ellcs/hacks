```
joern> var bad_strlen = ({cpg.method
         .name("(?i)strlen")
         .callIn
         .inAssignment
         .target
         .evalType("(g?)int")}).filter { c => c.lineNumber == Some(1385) }
         
