package com.learning.chapter3LinkedList;

public class LinkedList {

    private int length = 0;
    ListNode head;



    public LinkedList() {
    }

    //Insert a node at the beginning of the list
    public synchronized void insertAtBegin(ListNode node){
        node.setNext(head);
        head = node;
        length++;
    }

    //Insert at end of the list
    public synchronized void insertAtEnd(ListNode node){
        if (head == null)
            head = node;
        else{
            ListNode p,q;
            for(p = head; (q = p.getNext()) != null; p = q){
                p.setNext(node);
            }
            length++;
        }
    }

    public void insert (int data, int position) {
        if (position < 0){
            position = 0;
        }
        if(position > length){
            position = length;
        }
        if (head == null){
            head = new ListNode(data);
        }

        else if( position ==0){
            ListNode temp = new ListNode(data);
            temp.next = head;
            head = temp;
        }
        else {
            ListNode temp = head;
            for(int i=1; i<position; i++){
                temp = temp.getNext();
            }
            ListNode newNode = new ListNode(data);
            newNode.next = temp.next;
            temp.setNext(newNode);
            length++;
        }
    }

    public synchronized ListNode removeFrpmBegin() {
        //this will be a sentinal node
        ListNode node = head;
        if (node!=null){
            head = node.getNext();
            node.setNext(null);
        }
        return node;
    }









}
