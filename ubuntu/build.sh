#!/usr/bin/env bash
# Run through build-base.sh so shared image settings are available.
# Tags in the official-images manifest identify the supported
# Ubuntu OCI snapshots; all image bytes come from the org mirror.
curl -fsSL https://raw.githubusercontent.com/docker-library/official-images/master/library/ubuntu > ubuntu-library
mapfile -t releases < <(awk 'BEGIN {RS=""; FS="\n"} {tags=""; ref=""; for(i=1;i<=NF;i++) {if($i ~ /^Tags: /) {tags=$i; sub(/^Tags: /, "", tags)} if($i ~ /^amd64-GitFetch: /) {ref=$i; sub(/^amd64-GitFetch: /, "", ref)}} if(tags != "" && ref != "") print tags "|" ref}' ubuntu-library)
((${#releases[@]}))
for entry in "${releases[@]}"; do
  tags=${entry%%|*}; ref=${entry#*|}
  tag=${ref#refs/tags/}
  rm -rf source context
  git clone --quiet --depth=1 --filter=blob:none --branch "$tag" --sparse \
    "$mirror" source
  git -C source sparse-checkout set oci
  revision=$(git -C source rev-parse HEAD)
  manifest=$(jq -r '.manifests[0].digest | sub("^sha256:"; "")' source/oci/index.json)
  manifest_file="source/oci/blobs/sha256/$manifest"
  mkdir context
  printf 'FROM scratch\n' > context/Dockerfile
  layer_index=0
  while IFS=$'\t' read -r media_type digest; do
    [[ "$media_type" == application/vnd.oci.image.layer.v1.tar+gzip ]]
    layer=${digest#sha256:}
    layer_file="source/oci/blobs/sha256/$layer"
    tar -tf "$layer_file" > layer-contents.txt
    if grep -Eq '(^|/)\.wh\.' layer-contents.txt; then
      echo 'OCI whiteout layer requires a native OCI import.' >&2
      exit 1
    fi
    cp "$layer_file" "context/layer-$layer_index.tar.gz"
    printf 'ADD layer-%s.tar.gz /\n' "$layer_index" >> context/Dockerfile
    layer_index=$((layer_index + 1))
  done < <(jq -r '.layers[] | [.mediaType, .digest] | @tsv' "$manifest_file")
  ((layer_index > 0))
  config=$(jq -r '.config.digest | sub("^sha256:"; "")' "$manifest_file")
  jq -r '.config.Env[]? | "ENV " + .' "source/oci/blobs/sha256/$config" >> context/Dockerfile
  jq -r '.config.Cmd | "CMD " + tojson' "source/oci/blobs/sha256/$config" >> context/Dockerfile
  IFS=',' read -ra aliases <<< "$tags"
  for i in "${!aliases[@]}"; do aliases[$i]="${aliases[$i]// /}"; done
  publish "${aliases[0]}" "$revision" context context/Dockerfile "${aliases[@]:1}"
done
