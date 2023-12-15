/*
채널은 파이프로, 채널 오퍼레이터 <-를 통해 값을 주고받을 수 있음

map이나 slice처럼 채널도 쓰기 전에 채널임을 선언해줘야 함

    ch := make(chan int)
    ch <- v    // 채널 ch를 통해 v를 보냄.
    v := <-ch  // ch로부터 값을 전달받아, v에 할당.

채널은 디폴트로 상대방이 준비된 후 값을 주고받기 때문에, 별도의 동기화 과정이나 condition variable 설정 없이 goroutine을 쓸 수 있음
*/

package main

import (
    "fmt"
    "math"
)

func compute(fn func(float64, float64) float64) float64 {
    return fn(3, 4)
}

func main() {
    // ① 함수를 변수에 할당해, 변수를 함수처럼 씀
    hypot := func(x, y float64) float64 {
        return math.Sqrt(x*x + y*y)
    }
    fmt.Println("① 변수를 통해 함수 호출 : ", hypot(5, 12))
    
    // ② 함수를 compute 함수에 인자로 전달함
    fmt.Println("② 함수를 함수에 인자로 전달")
    fmt.Println("compute(hypot) :\t", compute(hypot))
    fmt.Println("compute(math.Pow) :\t", compute(math.Pow))
}
