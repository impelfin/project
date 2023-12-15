package main

import "fmt"

// ① 매개변수 타입, 리턴 타입은 이름 뒤에 지정해 줌
func add1(x int, y int) int {
    return x + y
}

// ② 매개변수 x, y가 같은 타입일 때에는 타입을 한 번만 명시해 줄 수 있음
func add2(x, y int) int {
    return x + y
}

func main() {
    fmt.Println("add1(x int, y int)의 결과 : ", add1(42, 13))
    fmt.Println("add2(x, y int)의 결과 : ", add2(42, 13))
}