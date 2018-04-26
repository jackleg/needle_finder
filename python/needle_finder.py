# -*- coding:utf-8 -*-


import sys
from collections import defaultdict, namedtuple

class NeedleFinder():
    """needle이 segment로 구성되어 있을 때, segment의 집합인 haystack 속에서 needle이 존재 가능한지 여부를 찾아낸다.

    예를 들어, neelde -> segments가 아래와 같고,
    A -> a, b, c
    B -> b, c, d
    C -> e

    haystack이 아래와 같다면,
    a, b, c, e, f, g

    haystack에서는 A, C needle이 존재 가능하다.

    Trie구조를 기반으로,
    edge는 dictionary의 key로 구현하며, segment를 뜻함.
    node는 root로부터 현재 노드까지의 path에 있는 segment들로 구성된 needle 정보를 object로 가지고 있다.
    """

    class Node:
        """현재 node까지의 path로 이루어진 needle과 하위 node들을 가지고 있음."""
        def __init__(self):
            self.needle_set = {}
            self.children = {}

        def insert(self, segment_list, needle, needle_info=None):
            """주어진 segment list로 따라 내려가서 needle_info 저장

            segment_list는 정렬되어 있어야 한다.
            """
            if segment_list:
                if segment_list[0] not in self.children:
                    self.children[segment_list[0]] = NeedleFinder.Node()

                return self.children[segment_list[0]].insert(segment_list[1:], needle, needle_info)

            # term_list가 비었다는 것은 값을 저장할 마지막 node까지 왔다는 뜻.
            else:
                self.needle_set[needle] = needle_info
                return self

        def traverse_by_segment_list(self, result_dict, segment_list, path):
            """현재 node와 segment_list로 children들을 traverse하면서 얻은 값들을 result_dict에 담아 반환한다.

            segment_list는 정렬되어 있어야 한다.
            """

            # 현재 node의 value
            for needle, needle_info in self.needle_set.iteritems():
                result_dict[needle] = needle_info

            # segment_list에 있는 값들로 traverse
            # [0:], [1:], ..., [-1:]과 같이 앞에서 하나씩 segment를 제거하면서 모든 경우를 찾는다.
            for index, segment in enumerate(segment_list):
                if segment in self.children:
                    self.children[segment].traverse_by_segment_list(result_dict, segment_list[index+1:], path + [segment])

            return len(result_dict)

        def preorder(self, path):
            for needle in self.needle_set:
                sys.stdout.write("%s\t%s\n" % ("|".join(path), needle))

            for segment, child in self.children.iteritems():
                child.preorder(path + [segment])


    def __init__(self):
        self.root = NeedleFinder.Node()

    def insert(self, segment_list, needle, needle_info=None, is_sorted=False):
        """Neelde Finder에 needle 정보 추가

        :param sorted: segment_list가 정렬되어 있는지 여부. default: False
        """

        list_to_add = segment_list if is_sorted else sorted(segment_list)
        self.root.insert(list_to_add, needle, needle_info)

    def traverse_by_segment_list(self, result_dict, segment_list, is_sorted=False):
        """segment_list에 있는 segment들을 따라가면서 이 graph에 있는 query 정보를 모두 수집.

        :param sorted: segment_list가 정렬되어 있는지 여부. default: False
        """

        list_to_traverse = segment_list if is_sorted else sorted(segment_list)
        return self.root.traverse_by_segment_list(result_dict, list_to_traverse, [])

    def preorder(self):
        self.root.preorder([])


if __name__ == "__main__":
    print "example"
    print "\tneedles"
    print "\t\tneedle: segments (data)"
    print "\t\tA: a b c (100)"
    print "\t\tB: b f (200)"
    print "\t\tC: b c e (150)"
    print "\t\tD: d f (900)"
    print "\thaystack"
    print "\t\ta b c e f "
    print ""

    # finder에 needle 정보 추가
    needle_finder = NeedleFinder()
    needle_finder.insert("a b c".split(), "A", 100)
    needle_finder.insert("b f".split(), "B", 200)
    needle_finder.insert("b c e".split(), "C", 150)
    needle_finder.insert("d f".split(), "D", 900)

    # haystack에서 needle 찾기
    result = {}
    result_count = needle_finder.traverse_by_segment_list(result, "a b c e f".split())

    # 결과 출력
    print "result"
    print "haystack에서 찾는 needle 개수: ", result_count
    print "찾은 needle과 needle 정보: ", result
