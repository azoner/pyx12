/*
######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

$Id$
*/

#ifndef PYX12_SEGMENT_HXX_
#define PYX12_SEGMENT_HXX_

#include <string>
#include <vector>
#include <stack>
#include <iostream>
#include <fstream>
#include <cstddef>
#include <memory>
#include <algorithm>

//#include <ostream>

using namespace std;

namespace Pyx12
{
/*
    class DataItem
    {
    public:
        virtual size_t length();
        virtual string format();
        virtual string getValue();
        //virtual void setValue(string);
        virtual bool isComposite();
        virtual bool isElement();
        virtual bool isEmpty();
    }
*/

    /** Element Class
     * Contains X12 element and sub-element values
     */
    class Element //: public DataItem
    {
    public:
        Element();
        Element(const string& ele_str);
        size_t length() const;
        string format();
        string getValue();
        void setValue(const string& ele_str);
        bool isComposite();
        bool isElement();
        bool isEmpty();
        friend ostream & operator << (ostream & out, Pyx12::Element & e);
        
    private:
        /// The element value
        string value;
    };

    typedef vector<Element> CompElements;
    typedef CompElements::size_type CompElements_sz;
    
    /** Composite Class
     * Contains X12 Composites(including simple elements)
     */
    class Composite //: public DataItem
    {
    public:
        Composite();
        Composite(const string& ele_str, const char subele_term_);
        Element& operator[](CompElements_sz);
        const Element& operator[](CompElements_sz) const;
        CompElements_sz length() const;
        string format();
        string format(const char subele_term_);
        string getValue();
        Element getElement(int comp_idx);
        void setValue(const string& ref_des, const string& val);
        void setValue(const CompElements_sz comp_idx, const string& val);
        void setSubeleTerm(const char subele_term_);
        bool isComposite();
        bool isElement();
        bool isEmpty();
        friend ostream & operator << (ostream & out, Pyx12::Composite & c);
//        bool not_delim(char c);
//        bool delim(char c);
//
    private:
        /// The elements making up this segment
        CompElements elements;
        
        /// Current sub-element delimiter
        char subele_term;
        
        /// Original sub-element delimiter
        char subele_term_orig;
        
        /** Split a composite string into elements
         *
         * @param ele_str A composite as a string
         */
        vector<string> split(const string& ele_str);
    };


    typedef vector<Composite> SegComposites;
    typedef SegComposites::size_type SegComposites_sz;
    
    /** Contains X12 Segments
     * A segment is comprised of a segment identifier and a sequence of elements.
     * 
     * An element can be a simple element or a composite.  A simple element is
     * treated as a composite element with one sub-element.
     * 
     * All indexing is zero based.
     */
    class Segment
    {
    public:
        Segment();
        Segment(const string& seg_str, const char seg_term_, 
            const char ele_term_, const char subele_term_);
        Composite& operator[](SegComposites_sz i);
        const Composite& operator[](SegComposites_sz i) const;
        Composite getComposite(const string& ref_des);
        const Composite getComposite(const string& ref_des) const;
        Element getElement(const string& ref_des);
        const Element getElement(const string& ref_des) const;
        void setValue(const string& ref_des, const string& val);
        void setValue(const SegComposites_sz comp_idx, const string& val);
        void append(const string& ele_str);
        SegComposites_sz length() const;
        string getSegId();
        string getValue(const string& ref_des);
        void setSegTerm(const char seg_term_);
        void setEleTerm(const char ele_term_);
        void setSubeleTerm(const char subele_term_);

        /** Get a formatted representation of the segment.
         */
        string format();

        /** Get a formatted representation of the segment, using other delimiters.
         */
        string format(const char seg_term_, const char ele_term_, const char subele_term_);
        void format_ele_list(vector<string> str_elems);
        void format_ele_list(vector<string> str_elems, const char subele_term_);
        bool isSegIdValid();
        bool isEmpty();
//        bool not_delim(char c);
//        bool delim(char c);
        friend ostream & operator << (ostream & os, Pyx12::Segment & seg);
        
    private:
        /// Current segment delimiter
        char seg_term;
        
        /// Original segment delimiter
        char seg_term_orig;
        
        /// Current element delimiter
        char ele_term;
        
        /// Original element delimiter
        char ele_term_orig;
        
        /// Current sub-element delimiter
        char subele_term;
        
        /// Original sub-element delimiter
        char subele_term_orig;
        
        /// Segment ID
        string seg_id;
        
        /// The composites making up this segment
        SegComposites elements;

        /** Split a segment string into elements
         *
         * @param ele_str A segment as a string
         */
        vector<string> split(const string& ele_str);
        //pair<SegComposites_sz, SegComposites_sz> parseRefDes(const std::string& ref_des);
        pair<int, int> parseRefDes(const std::string& ref_des);
    };


    class IsDelim
    {
    public:
        IsDelim(const char c) : term(c) {}

        bool operator() (const char c)
        {
            return (term == c);
        };
        
    private:
        char term;
    };


    class IsNotDelim
    {
    public:
        IsNotDelim(const char c) : term(c) {}

        bool operator() (const char c)
        {
            return (term != c);
        }
        
    private:
        char term;
    };
}
#endif // PYX12_SEGMENT_HXX_
