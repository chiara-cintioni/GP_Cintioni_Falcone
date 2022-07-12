package com.RIBO.demo12;

public class ENATree extends Tree<String> {

    private static ENATree ENATree;
    private Node<String> node;

    private ENATree(Node<String> node) {
        super(node);
    }

    public static  ENATree getInstance(){
        if(ENATree == null){
            Node<String> root = new Node<>("ENA: ");
            ENATree = new ENATree(root);
        }
        return ENATree;
    }


}
