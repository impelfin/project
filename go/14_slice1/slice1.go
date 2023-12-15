package main

import "fmt"

func main() {
    names := [4]string{
        "John",
        "Paul",
        "George",
        "Ringo",
    }
    fmt.Println("배열 names :", names)
    
    fmt.Println("① 슬라이스 선언")
    // 슬라이스 선언방법
    // ① 일반적인 선언방법 : 변수 선언과 비슷. 슬라이스타입은 []type
    var s1 []string = names[0:3]
    // ② 슬라이스도 var 키워드와 타입 명시를 생략할 수 있음
    s2 := names[0:2]
    
    fmt.Println("names[0:3] :", s1)
    fmt.Println("names[0:2] :", s2)
    
    // s1에서 값을 바꾸면 names, s1에서도 바뀐 값을 볼 수 있음
    fmt.Println("② 슬라이스로 값 변경")
    fmt.Println("s1[0]", s1[0])
    s1[0] = "XXX"
    fmt.Println("s1[0] = XXX 실행 후 s1 :", s1)
    fmt.Println("s1[0] = XXX 실행 후 s2 :", s2)
    fmt.Println("s1[0] = XXX 실행 후 names :", names)
    
    s2 = s1[0:2]
    fmt.Println("s2 = s1[0:2] 실행 후  s2 :", s2)
}
