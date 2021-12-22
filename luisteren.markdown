---
layout: page
title: luisteren
list_title: "De meest recente podcast"
---
De podcast komt wekelijks online op de Soundcloud-pagina van [Tim Gistelinck](https://soundcloud.com/tim-gistelinck){:target="_blank"}, en kort daarna op iTunes, Spotify, Google Podcasts … Aan de rechterzijde van deze pagina vind je subscribe buttons voor alle grote diensten.


<div class="most_recent_podcast">
  {%- if site.posts.size > 0 -%}
    <h2 class="post-list-heading">{{ page.list_title | default: "Posts" }}</h2>
    <ul class="post-list">
    {%- for post in site.categories[site.catcatonindex1] limit:1 -%}
      <li>
        {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
        <span class="post-meta">{{ post.date | date: date_format }}</span>
        <h3>
          {% if post.external_url %}
          <a href="{{ post.external_url }}" target="_blank">
              {% else %}
              <a href="{{ post.url | relative_url }}">
                  {% endif %}
                  {{ post.title }}
              </a>
        </h3>
        {%- if site.show_excerpts -%}
          {% if post.description %}
            {{ post.description }}
          {% else %}
           {{ post.excerpt }}
          {% endif %}
        {%- endif -%}
        {% if post.embed_player %}
         {%- if site.show_embedded-playeronindex -%}
           {% include embedded-player.html currPost=post %}
        {%- endif -%}
        {%- endif -%}
        {% include read-more.html currPost=post %}
      </li>
      {%- endfor -%}
  {%- endif -%}