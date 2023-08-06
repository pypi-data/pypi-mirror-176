

def lookup_addresses_TFIDF(addresses,linz,match_col):

    from sparse_dot_topn import awesome_cossim_topn
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    addresses = [join_address(addy) for addy in addresses]
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3,3))
    tf_idf_matrix_clean = vectorizer.fit_transform(linz[match_col])

    tf_idf_matrix_dirty = vectorizer.transform(linz[match_col])
    matches = awesome_cossim_topn(tf_idf_matrix_dirty, tf_idf_matrix_clean.transpose(), 1, 0)
    matches_df = get_matches_df(matches, addresses, linz[match_col], top=0)
    return matches_df