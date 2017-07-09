_termicoder_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _TERMICODER_COMPLETE=complete $1 ) )
    return 0
}

complete -F _termicoder_completion -o default termicoder;
