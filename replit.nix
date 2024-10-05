{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.graphviz  # Adiciona a dependência do Graphviz
    pkgs.pygraphviz  # Adiciona pygraphviz para suporte Python
  ];
}
