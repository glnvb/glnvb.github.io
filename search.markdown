---
layout: default
title: zoeken
icon: /data/search.svg
---

<h1>Zoeken</h1>

<input type="text" id="search-box" name="query" autofocus autocomplete="off">

<ul id="search-results" class="post-list"></ul>

<script>
  window.store = {
    {% for post in site.posts %}
      "{{ post.url | slugify }}": {
        "title": "{{ post.title | xml_escape }}",
        "author": "{{ post.author | xml_escape }}",
        "category": "{{ post.category | xml_escape }}",
        "description": "{{ post.description | xml_escape }}",
        "url": "{{ post.url | relative_url | xml_escape }}"

      }
      {% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
</script>
<script src="{{ '/js/lunr.min.js' | relative_url}}"></script>
<script src="{{ '/js/search.js' | relative_url}}"></script>


