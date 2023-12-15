package main

import "fmt"

type Vertex struct {
    X int
    Y int
}

// 구조체 인스턴스 선언 방법
var (
    // ① 일반적인 선언방식. X가1, Y가 2로 초기화 됨
    v1 = Vertex{1, 2}
    // ② X만 값을 지정해주고, Y는 int에  zero value로 설정됨
    v2 = Vertex{X: 1}
    // ③ X, Y모두 int에 zero value로 설정됨
    v3 = Vertex{}
)

func main() {
    fmt.Println("v1.X값 :", v1.X)
    v1.X = 4
    fmt.Println("v1.X = 4로 바꾼 v1.X값 :", v1.X)
    
    fmt.Printf("v2.X : %d, v2.Y : %d\n", v2.X, v2.Y)

    // ④ 구조체 포인터로도 구조체의 값을 바꿀 수 있음
    var p  = &v1
    p.X = 10
    fmt.Println("포인터로 바꾼 v1.X값 :", v1.X)
}
