package main

import "fmt"

// ① 변수를 하나 선언
var num1 int

// ② 같은 타입을 가지는 변수를 여러 개 선언
var num2, num3 int 

// ③ 여러 변수에 한 번에 값을 초기화 : 선언과 동시에 값을 초기화하면 타입을 명시할 필요가 없음
var num4, num5, str1 = 4, 5, "example" 

// ④ 함수 밖에서는 := 를 쓸 수 없음
// errorvar := str1

// ⑤ 다른 타입을 가지는 변수를 여러 개 선언
var (
    i int
    b bool
    s string
)

func main(){
    fmt.Println("①", num1)
    fmt.Println("②", num2, num3)
    fmt.Println("③", num4, num5, str1)
    
    // ④ 함수 안에서는 := 를 쓰면 var과 타입을 지정하지 않고 변수를 선언과 동시에 초기화 할 수 있음
    num6 := 6
    fmt.Println("④", num6)
    
    fmt.Println("⑤", i, b, s)
}
