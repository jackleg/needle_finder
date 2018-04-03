# 개요
정보의 단위를 segment라고 하고, 찾아야 할 대상(needle)이 segment의 조합으로 구성되어 있을 때,  
segment의 집합인 haystack에서 needle을 찾아낸다.

예를 들어, neelde(-> segments)가 아래와 같고,
* A -> a, b, c
* B -> b, c, d
* C -> e

haystack이 아래와 같다면,
* a, b, c, e, f, g

haystack에서는 A, C needle이 존재 가능하다.  
(B의 "d" segment가 haystack에 없다.)

# 사용법
1. NeedleFinder 생성
```
needle_finder = NeedleFinder()
```

2. NeedleFinder에 insert로 needle 정보를 추가
```
needle_finder.insert("a b c".split(), "A", 100)
needle_finder.insert("b f".split(), "B", 200)
needle_finder.insert("b c e".split(), "C", 150)
needle_finder.insert("d f".split(), "D", 900)
```

3. haystack과 결과를 담을 사전 객체를 전달.
```
result = {}
result_count = needle_finder.traverse_by_segment_list(result, "a b c e f".split())
```

4. 결과 사전 객체에는 {needle: needle_info} 사전이 전달됨.

# 결과 예시
```
> ./needle_finder.py
example
	needles
		needle: segments (data)
		A: a b c (100)
		B: b f (200)
		C: b c e (150)
		D: d f (900)
	haystack
		a b c e f 

result
haystack에서 찾는 needle 개수:  3
찾은 needle과 needle 정보:  {'A': 100, 'C': 150, 'B': 200}
```
