package main

import "fmt"

func main() {
    i, j := 42, 2701
    
    p := &i         // i를 가리키는 포인터
    fmt.Println(*p) // 포인터를 통해 i 값을 읽음
    *p = 21         // 포인터를 통해 i 값을 설정
    fmt.Println(i)
    
    p = &j         // j를 가리킴
    *p = *p / 37   // 포인터를 통해 j를 나눔
    fmt.Println(j)
}
