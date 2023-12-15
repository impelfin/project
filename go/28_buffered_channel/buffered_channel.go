/*
버퍼 길이와 시간(초 단위)을 make에 인자로 전달하면 buffered 채널을 만들 수 있음

    ch := make(chan int, 100)

이렇게 하면 buffered 채널은 버퍼가 꽉 찰 때까지 블락되거나(값을 전송할 때), 버퍼가 다 빌 때까지 블락됨 
(값을 전달받을 때).

코드를 실행하면 데드락이 발생함. 

24번째 줄을 수정해, 버퍼 크기를 키워보세요.

    ch := make(chan int, 1)

    ch := make(chan int, 10)
*/

package main

import "fmt"

func main() {
    // ① 버퍼크기가 1인 채널을 만듬
    // ch := make(chan int, 1)
    ch := make(chan int, 10)
    
    // ② 채널에 1을 전달합니다. 버퍼가 꽉 참
    ch <- 1

    // ③ 버퍼가 꽉 찬 상태에서 2를 또 전달 - 버퍼를 비워줄 루틴이 없어 데드락이 발생함
    ch <- 2

    fmt.Println(<-ch)
    fmt.Println(<-ch)
}
