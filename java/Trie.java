import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by 1003946 on 2018. 4. 20..
 */
public class Trie {
    private class Node {
        /** 현재 노드에서 사용 가능한 term들의 list
         *
         * term list의 list로 term list가 하나의 질의를 뜻한다
         * [[term1, term2], [term3, term4, term5], ...]
         */
        private ArrayList<ArrayList<String>> termsList;

        /** 현재 노드의 하위 노드
         * 노드 사이의 연결 String이 edge를 뜻함.
         */
        private HashMap<String, Node> children;

        private Node() {
            termsList = new ArrayList<ArrayList<String>>();
            children = new HashMap<String, Node>();
        }

        /** segmentList를 따라가다 마지막 node에서 term를 저장한다. */
        private Node insert(List<String> segmentList, ArrayList<String> terms) {
            // list가 빈 경우는 마지막까지 내려왔다는 뜻으로 저장한다.
            if(segmentList.isEmpty()) {
                termsList.add(terms);
                return this;
            }
            // 아래로 내려가야 함
            else {
                String key = segmentList.remove(0);

                if (children.containsKey(key) == false) {
                    children.put(key, new Node());
                }

                return children.get(key).insert(segmentList, terms);
            }
        }

        /** segmentList에 있는 segment들을 따라 children을 따라 내려가면서 노드들에 저장되어 있는 질의 정보를 list에 담아서 반환 */
        private int traverseBySegmentList(ArrayList<ArrayList<String>> resultList, List<String> segmentList) {
            // 현재 노드의 value 저장
            resultList.addAll(termsList);

            // segmentList를 하나씩 돌면서 모든 경우를 찾는다.
            int end = segmentList.size();

            for(int start=0;start < segmentList.size();start++) {
                String key = segmentList.get(start);

                if(children.containsKey(key)) {
                    children.get(key).traverseBySegmentList(resultList, segmentList.subList(start+1, end));
                }
            }

            return resultList.size();
        }
    }

    private Node root;

    public Trie() {
        root = new Node();
    }

    /** segmentList로 위치를 찾아서 termList를 저장한다. */
    public Node insert(List<String> segmentList, ArrayList<String> termList) {
        return root.insert(segmentList, termList);
    }

    /** segmentList에 있는 segment를 따라가면서 이 graph에 있는 terms 정보를 수집 */
    public int traverseBySegmentList(ArrayList<ArrayList<String>> resultList, List<String> segmentList) {
        return root.traverseBySegmentList(resultList, segmentList);
    }

    public static void main(String[] args) {
        Trie needleFinder = new Trie();

        ArrayList<String> seg = new ArrayList();
        seg.add("a");
        seg.add("b");
        seg.add("c");

        ArrayList<String> terms = new ArrayList();
        terms.add("A");
        terms.add("B");

        needleFinder.insert(seg, terms);

        ArrayList<String> seg2 = new ArrayList();
        seg2.add("b");
        seg2.add("f");

        ArrayList<String> terms2 = new ArrayList();
        terms2.add("B");
        terms2.add("D");

        needleFinder.insert(seg2, terms2);

        ArrayList<String> seg3 = new ArrayList();
        seg3.add("b");
        seg3.add("c");
        seg3.add("e");

        ArrayList<String> terms3 = new ArrayList();
        terms3.add("C");
        terms3.add("D");

        needleFinder.insert(seg3, terms3);

        ArrayList<String> seg4 = new ArrayList();
        seg4.add("d");
        seg4.add("f");

        ArrayList<String> terms4 = new ArrayList();
        terms4.add("D");
        terms4.add("E");

        needleFinder.insert(seg4, terms4);

        ArrayList<String> haystack = new ArrayList<>();
        haystack.add("a");
        haystack.add("b");
        haystack.add("c");
        haystack.add("e");

        ArrayList<ArrayList<String>> resultList = new ArrayList<>();
        int resultCount = needleFinder.traverseBySegmentList(resultList, haystack);

        System.out.println("result");
        System.out.println("haystack에서 찾은 needle 개수: " + resultCount);
        for(ArrayList<String>ts: resultList) {
            System.out.println(ts);
        }

    }
}
