/*
sender가 더 이상 보낼 값이 없어 채널을 닫으면 reciever가 이를 알아챌 수 있어야 함. 
채널이 열려있는지 닫혀있는지 알아내는 방법은 다음과 같다.

    v, ok := <-ch

채널로부터 더 이상 받을 값이 없고 채널이 닫혔다면, 두 번째 인자 ok가 false가 되며, 그렇지 않다면 ok는 true 임.

반복문 안에서 채널로부터 값을 전달받을 때에는 굳이 ok로 확인할 필요 없이, for i: range c를 써, 채널 c가 닫힐 때까지 값을 계속 전달받음

아래 코드를 실행하면 데드락이 발생함 

fibonacci 함수(sender)에서 채널을 닫지 않아, main의 for문(receiver)이 종료되지 않기 때문임

13번째 줄 close(c)의 주석을 지워보세요.

*주의1* 오직 sender만 채널을 닫아야 함. 
reciever가 채널을 닫아, 한쪽이 닫힌 채널에 데이터를 전송하면 패닉이 발생함.

*주의2* : 채널은 파일과는 다름.
보통은 닫을 필요 없고, 오직 sender가 "더 이상 보낼 값이 없다"는 뜻을 전달하는 의미에서 씀
*/

package main

import (
    "fmt"
)

// sender에 해당하는 코드
// 0번째부터 n번째까지의 피보나치수를 채널 c를 통해 전달한 후, 채널을 닫음
func fibonacci(n int, c chan int) {
    x, y := 0, 1
    for i := 0; i < n; i++ {
        c <- x
        x, y = y, x+y
    }
    close(c)
}

func main() {
    c := make(chan int, 10)
    go fibonacci(cap(c), c)
    // receiver에 해당하는 코드
    // fibonacci 함수로부터 값을 전달받으며, sender측에서 채널을 닫으면 반복문이 종료됨
    for i := range c {
        fmt.Println(i)
    }
}
