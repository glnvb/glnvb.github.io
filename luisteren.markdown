---
layout: page
title: luisteren
list_title: "De meest recente podcast"
---

De podcast komt wekelijks online op de Soundcloud-pagina van Tim Gistelinck en kort daarna op iTunes, Spotify, …

<div class="post-list">
{%- assign social = site.minima.social_links -%}
<ul class="luisteren-list">
  {%- if social.soundcloud -%}<li><a href="https://soundcloud.com/{{ social.soundcloud | cgi_escape | escape }}"
      title="SoundCloud"><img class="svg-icon grey" src="{{ '/assets/soundcloud.svg' | relative_url }}"
        onload="SVGInject(this)"></a><a href="https://soundcloud.com/{{ social.soundcloud | cgi_escape | escape }}">Soundcloud</a></li>{%- endif -%}
  {%- if social.itunesname -%}<li><a
      href="https://podcasts.apple.com/be/podcast/{{ social.itunesname | cgi_escape | escape }}/{{ social.itunesid | cgi_escape | escape }}"
      title="Apple iTunes"><img class="svg-icon grey" src="{{ '/assets/podcast.svg' | relative_url }}"
        onload="SVGInject(this)"></a><a href="https://podcasts.apple.com/be/podcast/{{ social.itunesname | cgi_escape | escape }}/{{ social.itunesid | cgi_escape | escape }}">iTunes Apple Podcasts</a></li>{%- endif -%}
 {%- if social.spotify -%}<li><a href="https://open.spotify.com/show/{{ social.spotify | cgi_escape | escape }}"
      title="Spotify"><img class="svg-icon grey" src="{{ '/assets/spotify.svg' | relative_url }}"
        onload="SVGInject(this)"></a><a href="https://open.spotify.com/show/{{ social.spotify | cgi_escape | escape }}">Spotify</a></li>{%- endif -%}
  {%- if social.youtube_channel -%}<li><a rel="me"
      href="https://www.youtube.com/channel/{{ social.youtube_channel | cgi_escape | escape }}" title="YouTube"><img
        class="svg-icon grey" src="{{ '/assets/youtube-square.svg' | relative_url }}" onload="SVGInject(this)"></a><a href="https://www.youtube.com/channel/{{ social.youtube_channel | cgi_escape | escape }}">Youtube (geen podcasts)</a></li>
  {%- endif -%}
</ul></div>



