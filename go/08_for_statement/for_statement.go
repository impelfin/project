package main

import "fmt"

func main() {
    // Type 1 : 기본 for statement
    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }
    fmt.Println(sum)
    
    // Type 2 : 조건식만 있는 for loop, 세미콜론 없이, C의 while과 비슷하게 쓸 수 있음
    sum = 1
    for sum < 1000 {
        sum += sum
    }
    fmt.Println(sum)
    
    // Type 3 : for range loop
    names := []string{"홍길동", "이순신", "강감찬"}
    for index, name := range names {
        println(index, name)
    }

    // Type 4 : for break continue goto
    var a = 1
    for a < 15 {
        if a == 5 {
            a += a
            continue // for loop 시작으로
        }
        a++
        if a > 10 {
            break // loop 빠져나옴
        }
        println("a value = ", a)
    }
    if a == 11 {
        goto END
    }
END:
    println("End")

    // Type 5 : for {} 무한 루프
    // for {
    //     println("Infinite loop")
    // }
}
