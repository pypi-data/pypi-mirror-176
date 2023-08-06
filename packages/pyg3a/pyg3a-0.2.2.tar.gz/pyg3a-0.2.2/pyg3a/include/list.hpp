#ifndef LIST_H_
#define LIST_H_

#include <stddef.h>

template <class T> class ListItem {
public:
  typedef T value_type;
  typedef T *ptr_type;

private:
  value_type item_val;
  ListItem *next_val;

  void setNext(ptr_type next) { next_val = next; }

  ptr_type getNext() { return next_val; }

public:
  ListItem(value_type data) {
    item_val(data);
    next_val(NULL);
  }
};

template <class T> class List {
private:
  typedef ListItem<T> list_item_type;
  typedef list_item_type *list_item_ptr;

public:
  typedef typename list_item_type::value_type value_type;

  void insert(value_type data);

private:
  list_item_ptr first, last;
};

template <class T> void List<T>::insert(value_type data) {
  if (first == NULL) {
    first = new list_item_type(data);
    last = first;
  } else {
    /* a */
    last.setNext(new list_item_type(data));
    list_item_ptr tmp = last;
    last = tmp.getNext();
  }
}

#endif // LIST_H_
