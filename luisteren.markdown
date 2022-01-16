---
layout: page
title: luisteren
list_title: "De meest recente podcast"
---

De podcast komt wekelijks online op de Soundcloud-pagina van Tim Gistelinck en kort daarna op iTunes, Spotify, …

{% assign social = site.minima.social_links %}
<div class="luisteren">
  {% if social.soundcloud %}<a href="https://soundcloud.com/{{ social.soundcloud | cgi_escape | escape }}"
      title="SoundCloud"><img class="svg-icon grey" src="{{ '/assets/soundcloud.svg' | relative_url }}"
        onload="SVGInject(this)"><p>Soundcloud</p></a>{% endif %}
  {% if social.itunesname %}<a
      href="https://podcasts.apple.com/be/podcast/{{ social.itunesname | cgi_escape | escape }}/{{ social.itunesid | cgi_escape | escape }}"
      title="Apple iTunes"><img class="svg-icon grey" src="{{ '/assets/podcast.svg' | relative_url }}"
        onload="SVGInject(this)"><p>iTunes Apple Podcasts</p></a>{% endif %}
 {% if social.spotify %}<a href="https://open.spotify.com/show/{{ social.spotify | cgi_escape | escape }}"
      title="Spotify"><img class="svg-icon grey" src="{{ '/assets/spotify.svg' | relative_url }}"
        onload="SVGInject(this)"><p>Spotify</p></a>{% endif %}
  <!-- {%- if social.youtube_channel -%}<a rel="me"
      href="https://www.youtube.com/channel/{{ social.youtube_channel | cgi_escape | escape }}" title="YouTube"><img
        class="svg-icon grey" src="{{ '/assets/youtube-square.svg' | relative_url }}" onload="SVGInject(this)"></a><p>Youtube (geen podcasts)</p>
  {%- endif -%} -->
</div>



