---
layout: page
title: zoeken
icon: /data/search.svg
---
u kan zoeken met de joker: *, de zoekmotor zoekt in de titel, beschrijving en de tags van de posts en artikels.

<input type="text" id="search-box" name="query" autofocus autocomplete="off">

<ul id="search-results" class="post-list"></ul>

<script>
  window.store = {
    {% for post in site.posts %}
      "{{ post.url | slugify }}": {
        "title": "{{ post.title | xml_escape }}",
        "author": "{{ post.author | xml_escape }}",
        "category": "{{ post.category | xml_escape }}",
        "tags": "{% for tag in post.tags %}{{ tag | xml_escape }} {% endfor %}",
        "description": "{{ post.description | xml_escape }}",
        "url": "{{ post.url | relative_url | xml_escape }}"

      }
      {% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
</script>
<script src="{{ '/js/lunr.min.js' | relative_url}}"></script>
<script src="{{ '/js/search.js' | relative_url}}"></script>


