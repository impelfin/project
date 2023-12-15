/*
Go 언어 기본 자료형
bool : true, false를 저장
string : 문자 / 문자열을 저장
int / int8 / int16 / int32 / int64 / uint / uint8 / uint16 / uint32 / uint64 / uintptr
byte : uint8과 같음
rune : int32와 같음. 유니코드 포인트를 나타냄
float32 / float 64
complex64 / complex128
*/

package main

import (
    "fmt"
    "math/cmplx"
)

var (
    i int = 5
    f float64
    MaxInt uint64 = 1 << 64 - 1
    z complex128 = cmplx.Sqrt(-5 + 12i)
)

func main() {
    const format = "%T(%v) \n"
    fmt.Printf(format, MaxInt, MaxInt)
    fmt.Printf(format, z, z)

    // int에서 float64로 묵시적 타입 변환을 할 수 없음
    // f = i
    
    // 다른 타입을 저장하려면 변환할타입(변수) 와 같이, 형 변환을 해줘야 함
    f = float64(i)
    fmt.Printf(format, f, f)
}
