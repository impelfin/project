package main

import "fmt"

type Vertex struct {
    Lat, Long float64
}

func main() {
    // ① map 사용
    // map[string] 타입 변수 선언
    var mymap map[string]Vertex
    // make()로 맵 생성
    mymap = make(map[string]Vertex)
    mymap["Bell Labs"] = Vertex{
        40.68433, -74.39967,
    }
    fmt.Println("① mymap[\"Bell Labs\"] :", mymap["Bell Labs"])

    // ② map literal 사용
    // 맵 리터럴은 구조체 리터럴에 key를 추가한 것과 같고, 맵 리터럴은 make함수가 필요 없음
    var mymap_literal = map[string]Vertex{
        "Bell Labs": Vertex{
            40.68433, -74.39967,
        },
        "Google": Vertex{
            37.42202, -122.08408,
        },
    }
    fmt.Println("② mymap_literal[\"Bell Labs\"] :", mymap_literal["Bell Labs"])
    fmt.Println("② mymap_literal[\"Google\"] :", mymap_literal["Google"])
}
