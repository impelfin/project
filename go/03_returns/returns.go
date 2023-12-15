package main

import "fmt"

// ① return 뒤에 리턴 타입을 적어주는 방법
func divide1(dividend, divisor int) (int, int) {
    var quotient = (int)(dividend / divisor)
    var remainder = dividend % divisor
    return quotient, remainder
}

// ② return 뒤에 리턴할 변수를 선언하는 방법. ① 과는 달리 함수 내부에서 `quotient`를 `var`로 선언하지 않고 바로 사용 가능
func divide2(dividend, divisor int) (quotient, remainder int) {
    quotient = (int)(dividend / divisor)
    remainder = dividend % divisor
    return // return 이라고만 적으면 미리 return 값으로 정해 놓은 quotient와 remainder를 return
}

func main() {
    // ① 로 한 번에 여러 개의 결과를 return 받는 부분
    var quotient, remainder int
    quotient, remainder = divide1(10, 3)
    fmt.Println("① 의 결과 :", quotient, remainder)
    
    // ② 로 한 번에 여러 개의 결과를 return 받는 부분
    quotient, remainder = divide2(10, 3)
    fmt.Println("② 의 결과 :", quotient, remainder)
}
