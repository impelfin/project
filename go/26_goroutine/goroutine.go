/*
goroutine은 Go runtime가 담당하는 경량(lightweight) 쓰레드 임

    go f(x, y, z)

는 다음의 새로운 goroutine을 실행하며, f, x, y, z의 값을 구하는 것은 현재 goroutine에서 진행되고, f를 실행하는 건 새로운 goroutine에서 진행됨

    f(x, y, z)

*주의* goroutine은 같은 주소 공간을 쓰기 때문에, shared memory에 접근할 때는 동기화 해줘야 함.
*/

package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func main() {
    go say("② another 루틴")
    say("① this 루틴")
}

