package main

import "fmt"

var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
    // ① 일반적인 range
    fmt.Println("① 일반적인 range")
    for i, v := range pow {
        fmt.Printf("2**%d = %d\n", i, v)
    }
    
    // ② 인덱스가 필요없는 경우 _로 비워둘 수 있음
    fmt.Println("② 인덱스가 필요없는 경우")
    for _, v := range pow {
        fmt.Println(v)
    }
}
