package com.RIBO.demo12;

import java.util.ArrayList;

public interface TreeInterface<T> {


    boolean isEmpty();

    Node getRoot();

    void setRoot(Node<T> root);

    boolean exists(T key);

    int size();

    int getNumberOfDescendants(Node<T> node);

    boolean find(Node<T> node, T keyNode);

    Node<T> findNode(Node<T> node, T keyNode);

    ArrayList<Node<T>> getPreOrderTraversal();

    ArrayList<Node<T>> getPostOrderTraversal();

    void buildPreOrder(Node<T> node, ArrayList<Node<T>> preOrder);

    void buildPostOrder(Node<T> node, ArrayList<Node<T>> postOrder);

    ArrayList<Node<T>> getLongestPathFromRootToAnyLeaf();

    int getHeight();

    ArrayList<ArrayList<Node<T>>> getPathsFromRootToAnyLeaf();

    void getPath(Node<T> node, ArrayList<Node<T>> currentPath,
                 ArrayList<ArrayList<Node<T>>> paths);

    ArrayList<Node<T>> clone(ArrayList<Node<T>> list);
}
