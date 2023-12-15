package main

import (
    "fmt"
)

var (
    i int // zero value = 0
    f float64 // zero value = 0
    b bool // zero value = false
    s string // zero value = ""
)

func main() {
    fmt.Printf("int의 zero value : %v\n", i)
    fmt.Printf("float64의 zero value : %v\n", f)
    fmt.Printf("boolean의 zero value : %v\n", b)
    fmt.Printf("string의 zero value : %q\n", s)
}
