### 1.1.1

#### Fix

+ Fixed flushing to file removing ansi and TED markup

___

### 1.1.0

#### New

+ Add custom logging
  * This allows for logging to file and to stdout
  * Custom labels
  * Custom messages
  * Custom logging levels
  * Method chaining
  * Global instance
  * Buffers until flushed

___

### 1.0.0

#### New

+ Add TED markup parser
  * Parse
    * Hyperlinks
    * Precise colors; foreground, background, both
    * Custom functions - Custom functions manipulate the next plain text block
  * Print
  * Define custome functions
