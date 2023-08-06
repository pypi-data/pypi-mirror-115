#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/include/builtins/ValueError.hpp>
#include <pythonic/include/builtins/abs.hpp>
#include <pythonic/include/builtins/assert.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/list.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/pythran/static_list.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/abs.hpp>
#include <pythonic/include/numpy/append.hpp>
#include <pythonic/include/numpy/argmin.hpp>
#include <pythonic/include/numpy/argsort.hpp>
#include <pythonic/include/numpy/array.hpp>
#include <pythonic/include/numpy/complex128.hpp>
#include <pythonic/include/numpy/concatenate.hpp>
#include <pythonic/include/numpy/conj.hpp>
#include <pythonic/include/numpy/convolve.hpp>
#include <pythonic/include/numpy/delete_.hpp>
#include <pythonic/include/numpy/diff.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/finfo.hpp>
#include <pythonic/include/numpy/float64.hpp>
#include <pythonic/include/numpy/isreal.hpp>
#include <pythonic/include/numpy/lexsort.hpp>
#include <pythonic/include/numpy/nonzero.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/numpy/zeros_like.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/invert.hpp>
#include <pythonic/include/operator_/le.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mod.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/not_.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/ValueError.hpp>
#include <pythonic/builtins/abs.hpp>
#include <pythonic/builtins/assert.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/list.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/pythran/static_list.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/abs.hpp>
#include <pythonic/numpy/append.hpp>
#include <pythonic/numpy/argmin.hpp>
#include <pythonic/numpy/argsort.hpp>
#include <pythonic/numpy/array.hpp>
#include <pythonic/numpy/complex128.hpp>
#include <pythonic/numpy/concatenate.hpp>
#include <pythonic/numpy/conj.hpp>
#include <pythonic/numpy/convolve.hpp>
#include <pythonic/numpy/delete_.hpp>
#include <pythonic/numpy/diff.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/finfo.hpp>
#include <pythonic/numpy/float64.hpp>
#include <pythonic/numpy/isreal.hpp>
#include <pythonic/numpy/lexsort.hpp>
#include <pythonic/numpy/nonzero.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/numpy/zeros_like.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/invert.hpp>
#include <pythonic/operator_/le.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mod.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/not_.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__zpk_funcs
{
  struct poly
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef std::integral_constant<long, 1> __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
      typedef typename pythonic::assignable<decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type4>()))>::type __type5;
      typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type5>())) __type6;
      typedef typename pythonic::lazy<__type6>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::convolve{})>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type10;
      typedef long __type11;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type13;
      typedef decltype(std::declval<__type13>()(std::declval<__type4>())) __type14;
      typedef decltype(std::declval<__type12>()(std::declval<__type14>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef decltype(std::declval<__type4>()[std::declval<__type16>()]) __type17;
      typedef decltype(pythonic::operator_::neg(std::declval<__type17>())) __type18;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type18>())) __type19;
      typedef decltype(std::declval<__type10>()(std::declval<__type19>())) __type20;
      typedef decltype(std::declval<__type9>()(std::declval<__type20>(), std::declval<__type5>())) __type21;
      typedef pythonic::types::str __type22;
      typedef decltype(std::declval<__type8>()(std::declval<__type7>(), std::declval<__type21>(), std::declval<__type22>())) __type23;
      typedef typename pythonic::lazy<__type23>::type __type24;
      typedef typename pythonic::returnable<typename __combined<__type7,__type24>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    typename type<argument_type0>::result_type operator()(argument_type0&& zeros) const
    ;
  }  ;
  struct _nearest_real_complex_idx
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argsort{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef decltype(pythonic::operator_::sub(std::declval<__type2>(), std::declval<__type3>())) __type4;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type5>()))>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type8;
      typedef decltype(std::declval<__type2>()[std::declval<__type6>()]) __type9;
      typedef decltype(std::declval<__type8>()(std::declval<__type9>())) __type10;
      typedef typename pythonic::lazy<__type10>::type __type11;
      typedef decltype(pythonic::operator_::invert(std::declval<__type11>())) __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef typename __combined<__type11,__type13>::type __type14;
      typedef decltype(std::declval<__type7>()(std::declval<__type14>())) __type15;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type15>::type>::type __type16;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type16>::type>::type __type17;
      typedef typename pythonic::returnable<decltype(std::declval<__type6>()[std::declval<__type17>()])>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& fro, argument_type1&& to, argument_type2&& which) const
    ;
  }  ;
  struct _cplxreal
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::lexsort{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type1>())) __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type1>())) __type6;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type6>())) __type7;
      typedef decltype(std::declval<__type2>()(std::declval<__type7>())) __type8;
      typedef decltype(std::declval<__type1>()[std::declval<__type8>()]) __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type11;
      typedef std::integral_constant<long, 0> __type12;
      typedef decltype(std::declval<__type11>()(std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type14;
      typedef decltype(std::declval<__type10>()(std::declval<__type13>(), std::declval<__type14>())) __type15;
      typedef typename pythonic::assignable<decltype(std::declval<__type1>()[std::declval<__type8>()])>::type __type16;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type16>())) __type17;
      typedef decltype(std::declval<__type3>()(std::declval<__type17>())) __type18;
      typedef long __type19;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::finfo{})>::type>::type __type20;
      typedef double __type21;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type1>())) __type22;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type22>())) __type23;
      typedef decltype(std::declval<__type20>()(std::declval<__type23>())) __type24;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::EPS{}, std::declval<__type24>())) __type25;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type25>()))>::type __type26;
      typedef decltype(std::declval<__type3>()(std::declval<__type16>())) __type27;
      typedef decltype(pythonic::operator_::mul(std::declval<__type26>(), std::declval<__type27>())) __type28;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::le(std::declval<__type18>(), std::declval<__type28>()))>::type __type29;
      typedef decltype(std::declval<__type16>()[std::declval<__type29>()]) __type30;
      typedef typename pythonic::assignable<decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type30>()))>::type __type31;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::invert(std::declval<__type29>())) __type33;
      typedef typename pythonic::assignable<decltype(std::declval<__type16>()[std::declval<__type33>()])>::type __type34;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type34>())) __type35;
      typedef decltype(pythonic::operator_::gt(std::declval<__type35>(), std::declval<__type19>())) __type36;
      typedef typename pythonic::assignable<decltype(std::declval<__type34>()[std::declval<__type36>()])>::type __type37;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type38;
      typedef decltype(pythonic::operator_::lt(std::declval<__type35>(), std::declval<__type19>())) __type39;
      typedef typename pythonic::assignable<decltype(std::declval<__type34>()[std::declval<__type39>()])>::type __type40;
      typedef decltype(std::declval<__type38>()(std::declval<__type40>())) __type41;
      typedef decltype(pythonic::operator_::add(std::declval<__type37>(), std::declval<__type41>())) __type42;
      typedef decltype(pythonic::operator_::div(std::declval<__type42>(), std::declval<__type19>())) __type43;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type43>(), std::declval<__type31>())) __type44;
      typedef __type0 __ptype0;
      typedef __type9 __ptype1;
      typedef typename pythonic::returnable<typename __combined<__type32,__type44>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    typename type<argument_type0>::result_type operator()(argument_type0&& z) const
    ;
  }  ;
  struct zpk2tf
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef poly __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type3>())) __type4;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
      typedef decltype(std::declval<__type1>()(std::declval<__type6>())) __type7;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type7>())) __type8;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type8>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
    ;
  }  ;
  struct zpk2sos
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef std::integral_constant<long, 6> __type5;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type6>()))>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type8;
      typedef decltype(std::declval<__type8>()(std::declval<__type4>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef indexable<__type10> __type11;
      typedef typename __combined<__type7,__type11>::type __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type13;
      typedef zpk2tf __type14;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros_like{})>::type>::type __type15;
      typedef std::integral_constant<long, 2> __type16;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>(), std::declval<__type16>())) __type17;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type18;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type17>(), std::declval<__type18>()))>::type __type19;
      typedef typename pythonic::assignable<decltype(std::declval<__type15>()(std::declval<__type19>()))>::type __type20;
      typedef typename __combined<__type20,__type11>::type __type21;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type22;
      typedef _cplxreal __type23;
      typedef typename pythonic::lazy<__type0>::type __type24;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::append{})>::type>::type __type25;
      typedef long __type26;
      typedef decltype(std::declval<__type25>()(std::declval<__type24>(), std::declval<__type26>())) __type27;
      typedef typename pythonic::lazy<__type27>::type __type28;
      typedef typename __combined<__type24,__type28>::type __type29;
      typedef typename _cplxreal::type<__type29>::__ptype0 __type30;
      typedef typename __combined<__type29,__type30>::type __type31;
      typedef typename _cplxreal::type<__type31>::__ptype1 __type32;
      typedef container<typename std::remove_reference<__type32>::type> __type33;
      typedef typename __combined<__type31,__type33>::type __type34;
      typedef decltype(std::declval<__type23>()(std::declval<__type34>())) __type35;
      typedef typename pythonic::assignable<decltype(std::declval<__type13>()(std::declval<__type35>()))>::type __type36;
      typedef _nearest_real_complex_idx __type37;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type38;
      typedef typename pythonic::assignable<decltype(std::declval<__type25>()(std::declval<__type38>(), std::declval<__type26>()))>::type __type39;
      typedef typename __combined<__type38,__type39>::type __type40;
      typedef typename _cplxreal::type<__type40>::__ptype0 __type41;
      typedef typename __combined<__type40,__type41>::type __type42;
      typedef typename _cplxreal::type<__type42>::__ptype1 __type43;
      typedef container<typename std::remove_reference<__type43>::type> __type44;
      typedef typename __combined<__type42,__type44>::type __type45;
      typedef decltype(std::declval<__type23>()(std::declval<__type45>())) __type46;
      typedef typename pythonic::assignable<decltype(std::declval<__type13>()(std::declval<__type46>()))>::type __type47;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argmin{})>::type>::type __type48;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type49;
      typedef decltype(std::declval<__type49>()(std::declval<__type47>())) __type50;
      typedef decltype(pythonic::operator_::sub(std::declval<__type26>(), std::declval<__type50>())) __type51;
      typedef decltype(std::declval<__type49>()(std::declval<__type51>())) __type52;
      typedef typename pythonic::assignable<decltype(std::declval<__type48>()(std::declval<__type52>()))>::type __type53;
      typedef typename pythonic::assignable<decltype(std::declval<__type47>()[std::declval<__type53>()])>::type __type54;
      typedef pythonic::types::str __type55;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type36>(), std::declval<__type54>(), std::declval<__type55>()))>::type __type56;
      typedef typename pythonic::assignable<decltype(std::declval<__type36>()[std::declval<__type56>()])>::type __type57;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::delete_{})>::type>::type __type58;
      typedef typename pythonic::assignable<decltype(std::declval<__type58>()(std::declval<__type36>(), std::declval<__type56>()))>::type __type59;
      typedef typename __combined<__type36,__type59>::type __type60;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type60>(), std::declval<__type54>(), std::declval<__type55>()))>::type __type61;
      typedef decltype(pythonic::operator_::sub(std::declval<__type54>(), std::declval<__type60>())) __type62;
      typedef decltype(std::declval<__type49>()(std::declval<__type62>())) __type63;
      typedef typename pythonic::assignable<decltype(std::declval<__type48>()(std::declval<__type63>()))>::type __type64;
      typedef typename __combined<__type61,__type64>::type __type65;
      typedef typename pythonic::assignable<decltype(std::declval<__type60>()[std::declval<__type65>()])>::type __type66;
      typedef typename __combined<__type57,__type66>::type __type67;
      typedef typename pythonic::assignable<long>::type __type68;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type69;
      typedef typename pythonic::assignable<decltype(std::declval<__type69>()(std::declval<__type67>()))>::type __type70;
      typedef typename __combined<__type68,__type70>::type __type71;
      typedef typename pythonic::assignable<decltype(std::declval<__type58>()(std::declval<__type60>(), std::declval<__type65>()))>::type __type72;
      typedef typename __combined<__type60,__type72>::type __type73;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type73>(), std::declval<__type54>(), std::declval<__type55>()))>::type __type74;
      typedef typename pythonic::assignable<decltype(std::declval<__type73>()[std::declval<__type74>()])>::type __type75;
      typedef typename __combined<__type71,__type75>::type __type76;
      typedef typename pythonic::assignable<decltype(std::declval<__type58>()(std::declval<__type73>(), std::declval<__type74>()))>::type __type77;
      typedef typename __combined<__type73,__type77>::type __type78;
      typedef typename pythonic::assignable<decltype(std::declval<__type69>()(std::declval<__type54>()))>::type __type79;
      typedef typename __combined<__type68,__type79>::type __type80;
      typedef typename pythonic::assignable<decltype(std::declval<__type58>()(std::declval<__type47>(), std::declval<__type53>()))>::type __type81;
      typedef typename __combined<__type47,__type81>::type __type82;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type82>(), std::declval<__type67>(), std::declval<__type55>()))>::type __type83;
      typedef typename pythonic::assignable<decltype(std::declval<__type82>()[std::declval<__type83>()])>::type __type84;
      typedef typename __combined<__type80,__type84>::type __type85;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type86;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type87;
      typedef decltype(std::declval<__type87>()(std::declval<__type82>())) __type88;
      typedef decltype(std::declval<__type86>()(std::declval<__type88>())) __type89;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type89>::type>::type>::type __type90;
      typedef decltype(std::declval<__type82>()[std::declval<__type90>()]) __type91;
      typedef decltype(std::declval<__type49>()(std::declval<__type91>())) __type92;
      typedef decltype(pythonic::operator_::sub(std::declval<__type92>(), std::declval<__type26>())) __type93;
      typedef decltype(std::declval<__type49>()(std::declval<__type93>())) __type94;
      typedef decltype(std::declval<__type48>()(std::declval<__type94>())) __type95;
      typedef typename pythonic::assignable<decltype(std::declval<__type90>()[std::declval<__type95>()])>::type __type96;
      typedef typename __combined<__type83,__type96>::type __type97;
      typedef typename pythonic::assignable<decltype(std::declval<__type82>()[std::declval<__type97>()])>::type __type98;
      typedef typename __combined<__type85,__type98>::type __type99;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type78>(), std::declval<__type99>(), std::declval<__type55>()))>::type __type100;
      typedef typename pythonic::assignable<decltype(std::declval<__type78>()[std::declval<__type100>()])>::type __type101;
      typedef typename __combined<__type76,__type101>::type __type102;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type67>(), std::declval<__type102>())) __type103;
      typedef decltype(std::declval<__type22>()(std::declval<__type103>())) __type104;
      typedef container<typename std::remove_reference<__type104>::type> __type105;
      typedef typename __combined<__type21,__type105>::type __type106;
      typedef pythonic::types::slice __type107;
      typedef typename pythonic::assignable<decltype(std::declval<__type106>()[std::declval<__type107>()])>::type __type108;
      typedef decltype(std::declval<__type108>()[std::declval<__type10>()]) __type109;
      typedef typename __combined<__type19,__type11>::type __type110;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type54>(), std::declval<__type99>())) __type111;
      typedef decltype(std::declval<__type22>()(std::declval<__type111>())) __type112;
      typedef container<typename std::remove_reference<__type112>::type> __type113;
      typedef typename __combined<__type110,__type113>::type __type114;
      typedef typename pythonic::assignable<decltype(std::declval<__type114>()[std::declval<__type107>()])>::type __type115;
      typedef decltype(std::declval<__type115>()[std::declval<__type10>()]) __type116;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type117;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type118;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type119;
      typedef decltype(std::declval<__type118>()(std::declval<__type119>())) __type120;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type120>())) __type121;
      typedef typename pythonic::assignable<decltype(std::declval<__type117>()(std::declval<__type4>(), std::declval<__type121>()))>::type __type122;
      typedef indexable<__type26> __type123;
      typedef typename __combined<__type122,__type123>::type __type124;
      typedef container<typename std::remove_reference<__type119>::type> __type125;
      typedef typename __combined<__type124,__type125>::type __type126;
      typedef decltype(std::declval<__type126>()[std::declval<__type10>()]) __type127;
      typedef decltype(std::declval<__type14>()(std::declval<__type109>(), std::declval<__type116>(), std::declval<__type127>())) __type128;
      typedef decltype(std::declval<__type13>()(std::declval<__type128>())) __type129;
      typedef container<typename std::remove_reference<__type129>::type> __type130;
      typedef __type0 __ptype2;
      typedef __type1 __ptype3;
      typedef typename pythonic::returnable<typename __combined<__type12,__type130>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k, argument_type3&& n_sections) const
    ;
  }  ;
  struct zpk2sos_multiple
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type5;
      typedef typename pythonic::assignable<decltype(std::declval<__type4>()(std::declval<__type5>()))>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type8;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type9;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type10;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type10>())) __type11;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type11>::type>::type __type12;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type9>())) __type13;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type13>::type>::type __type14;
      typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type14>())) __type15;
      typedef long __type16;
      typedef typename __combined<__type15,__type16>::type __type17;
      typedef decltype(std::declval<__type7>()(std::declval<__type17>(), std::declval<__type16>())) __type18;
      typedef decltype(std::declval<__type3>()(std::declval<__type18>(), std::declval<__type6>())) __type19;
      typedef decltype(std::declval<__type2>()(std::declval<__type19>())) __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type21>(), std::declval<__type16>()))>::type __type22;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type22>())) __type23;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
      typedef decltype(pythonic::operator_::sub(std::declval<__type24>(), std::declval<__type12>())) __type25;
      typedef typename __combined<__type25,__type16>::type __type26;
      typedef decltype(std::declval<__type7>()(std::declval<__type26>(), std::declval<__type16>())) __type27;
      typedef decltype(std::declval<__type3>()(std::declval<__type27>(), std::declval<__type6>())) __type28;
      typedef decltype(std::declval<__type2>()(std::declval<__type28>())) __type29;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type10>(), std::declval<__type29>())) __type30;
      typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type30>(), std::declval<__type16>()))>::type __type31;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type31>())) __type32;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type32>::type>::type __type33;
      typedef typename __combined<__type24,__type33>::type __type34;
      typedef decltype(std::declval<__type7>()(std::declval<__type34>(), std::declval<__type33>())) __type35;
      typedef decltype(pythonic::operator_::add(std::declval<__type35>(), std::declval<__type16>())) __type36;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type36>(), std::declval<__type16>()))>::type __type37;
      typedef std::integral_constant<long, 6> __type38;
      typedef decltype(std::declval<__type3>()(std::declval<__type6>(), std::declval<__type37>(), std::declval<__type38>())) __type39;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type39>()))>::type __type40;
      typedef zpk2sos __type41;
      typedef pythonic::types::contiguous_slice __type42;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type43;
      typedef decltype(std::declval<__type43>()(std::declval<__type6>())) __type44;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type44>::type::iterator>::value_type>::type __type45;
      typedef decltype(std::declval<__type31>()(std::declval<__type42>(), std::declval<__type45>())) __type46;
      typedef decltype(std::declval<__type22>()(std::declval<__type42>(), std::declval<__type45>())) __type47;
      typedef decltype(std::declval<__type5>()[std::declval<__type45>()]) __type48;
      typedef decltype(std::declval<__type41>()(std::declval<__type46>(), std::declval<__type47>(), std::declval<__type48>(), std::declval<__type37>())) __type49;
      typedef container<typename std::remove_reference<__type49>::type> __type50;
      typedef __type0 __ptype8;
      typedef __type1 __ptype9;
      typedef typename pythonic::returnable<typename __combined<__type40,__type50>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
    ;
  }  ;
  template <typename argument_type0 >
  typename poly::type<argument_type0>::result_type poly::operator()(argument_type0&& zeros) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef std::integral_constant<long, 1> __type2;
    typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
    typedef typename pythonic::assignable<decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type4>()))>::type __type5;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type5>())) __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::convolve{})>::type>::type __type8;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type10;
    typedef long __type11;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type12;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type13;
    typedef decltype(std::declval<__type13>()(std::declval<__type4>())) __type14;
    typedef decltype(std::declval<__type12>()(std::declval<__type14>())) __type15;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
    typedef decltype(std::declval<__type4>()[std::declval<__type16>()]) __type17;
    typedef decltype(pythonic::operator_::neg(std::declval<__type17>())) __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type18>())) __type19;
    typedef decltype(std::declval<__type10>()(std::declval<__type19>())) __type20;
    typedef decltype(std::declval<__type9>()(std::declval<__type20>(), std::declval<__type5>())) __type21;
    typedef pythonic::types::str __type22;
    typedef decltype(std::declval<__type8>()(std::declval<__type7>(), std::declval<__type21>(), std::declval<__type22>())) __type23;
    typedef typename pythonic::lazy<__type23>::type __type24;
    typedef typename __combined<__type7,__type24>::type __type25;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type>::type k;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, zeros))>::type dt = pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, zeros);
    typename pythonic::lazy<__type25>::type a = pythonic::numpy::functor::ones{}(pythonic::builtins::pythran::functor::make_shape{}(std::integral_constant<long, 1>{}), dt);
    {
      long  __target139918932644336 = pythonic::builtins::functor::len{}(zeros);
      for (long  k=0L; k < __target139918932644336; k += 1L)
      {
        a = pythonic::numpy::functor::convolve{}(a, pythonic::numpy::functor::array{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(1L, pythonic::operator_::neg(zeros.fast(k)))), dt), pythonic::types::str("full"));
      }
    }
    return a;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename _nearest_real_complex_idx::type<argument_type0, argument_type1, argument_type2>::result_type _nearest_real_complex_idx::operator()(argument_type0&& fro, argument_type1&& to, argument_type2&& which) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argsort{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
    typedef decltype(pythonic::operator_::sub(std::declval<__type1>(), std::declval<__type4>())) __type5;
    typedef decltype(std::declval<__type3>()(std::declval<__type5>())) __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type6>()))>::type __type7;
    typedef decltype(std::declval<__type1>()[std::declval<__type7>()]) __type8;
    typedef decltype(std::declval<__type0>()(std::declval<__type8>())) __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(pythonic::operator_::invert(std::declval<__type10>())) __type11;
    typedef typename pythonic::lazy<__type11>::type __type12;
    typedef typename __combined<__type10,__type12>::type __type13;
    typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::argsort{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(fro, to))))>::type order = pythonic::numpy::functor::argsort{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(fro, to)));
    typename pythonic::lazy<__type13>::type mask = pythonic::numpy::functor::isreal{}(fro.fast(order));
    if (pythonic::operator_::eq(which, pythonic::types::str("complex")))
    {
      mask = pythonic::operator_::invert(mask);
    }
    return order[std::get<0>(std::get<0>(pythonic::numpy::functor::nonzero{}(mask)))];
  }
  template <typename argument_type0 >
  typename _cplxreal::type<argument_type0>::result_type _cplxreal::operator()(argument_type0&& z) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::lexsort{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type2;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type0>())) __type3;
    typedef decltype(std::declval<__type2>()(std::declval<__type3>())) __type4;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type0>())) __type5;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type5>())) __type6;
    typedef decltype(std::declval<__type1>()(std::declval<__type6>())) __type7;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()[std::declval<__type7>()])>::type __type8;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type8>())) __type9;
    typedef decltype(std::declval<__type2>()(std::declval<__type9>())) __type10;
    typedef long __type11;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::finfo{})>::type>::type __type12;
    typedef double __type13;
    typedef decltype(pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type0>())) __type14;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type14>())) __type15;
    typedef decltype(std::declval<__type12>()(std::declval<__type15>())) __type16;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::EPS{}, std::declval<__type16>())) __type17;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type11>(), std::declval<__type17>()))>::type __type18;
    typedef decltype(std::declval<__type2>()(std::declval<__type8>())) __type19;
    typedef decltype(pythonic::operator_::mul(std::declval<__type18>(), std::declval<__type19>())) __type20;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::le(std::declval<__type10>(), std::declval<__type20>()))>::type __type21;
    typedef decltype(pythonic::operator_::invert(std::declval<__type21>())) __type22;
    typedef typename pythonic::assignable<decltype(std::declval<__type8>()[std::declval<__type22>()])>::type __type23;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type23>())) __type24;
    typedef decltype(pythonic::operator_::gt(std::declval<__type24>(), std::declval<__type11>())) __type25;
    typedef typename pythonic::assignable<decltype(std::declval<__type23>()[std::declval<__type25>()])>::type __type26;
    typedef pythonic::types::contiguous_slice __type27;
    typedef typename pythonic::assignable<decltype(std::declval<__type26>()[std::declval<__type27>()])>::type __type28;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type29;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type28>())) __type30;
    typedef decltype(std::declval<__type2>()(std::declval<__type30>())) __type31;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>())) __type32;
    typedef decltype(std::declval<__type29>()(std::declval<__type32>())) __type33;
    typedef decltype(std::declval<__type1>()(std::declval<__type33>())) __type34;
    typedef decltype(std::declval<__type28>()[std::declval<__type34>()]) __type35;
    typedef decltype(pythonic::operator_::lt(std::declval<__type24>(), std::declval<__type11>())) __type36;
    typedef typename pythonic::assignable<decltype(std::declval<__type23>()[std::declval<__type36>()])>::type __type37;
    typedef typename pythonic::assignable<decltype(std::declval<__type37>()[std::declval<__type27>()])>::type __type38;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type38>())) __type39;
    typedef decltype(std::declval<__type2>()(std::declval<__type39>())) __type40;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type40>())) __type41;
    typedef decltype(std::declval<__type29>()(std::declval<__type41>())) __type42;
    typedef decltype(std::declval<__type1>()(std::declval<__type42>())) __type43;
    typedef decltype(std::declval<__type38>()[std::declval<__type43>()]) __type44;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type45;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type46;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type47;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::diff{})>::type>::type __type48;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type49;
    typedef pythonic::types::list<typename std::remove_reference<__type11>::type> __type50;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type26>())) __type51;
    typedef decltype(std::declval<__type48>()(std::declval<__type51>())) __type52;
    typedef decltype(std::declval<__type26>()[std::declval<__type27>()]) __type53;
    typedef decltype(std::declval<__type2>()(std::declval<__type53>())) __type54;
    typedef decltype(pythonic::operator_::mul(std::declval<__type18>(), std::declval<__type54>())) __type55;
    typedef decltype(pythonic::operator_::le(std::declval<__type52>(), std::declval<__type55>())) __type56;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type50>(), std::declval<__type56>(), std::declval<__type50>())) __type57;
    typedef decltype(std::declval<__type49>()(std::declval<__type57>())) __type58;
    typedef typename pythonic::assignable<decltype(std::declval<__type48>()(std::declval<__type58>()))>::type __type59;
    typedef decltype(pythonic::operator_::gt(std::declval<__type59>(), std::declval<__type11>())) __type60;
    typedef decltype(std::declval<__type47>()(std::declval<__type60>())) __type61;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type61>::type>::type>::type __type62;
    typedef decltype(std::declval<__type46>()(std::declval<__type62>())) __type63;
    typedef decltype(std::declval<__type45>()(std::declval<__type63>())) __type64;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type64>::type::iterator>::value_type>::type>::type i;
    typename pythonic::assignable_noescape<decltype(z)>::type z_ = z;
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::mul(100L, pythonic::builtins::getattr(pythonic::types::attr::EPS{}, pythonic::numpy::functor::finfo{}(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::operator_::mul(1.0, z_))))))>::type tol = pythonic::operator_::mul(100L, pythonic::builtins::getattr(pythonic::types::attr::EPS{}, pythonic::numpy::functor::finfo{}(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::operator_::mul(1.0, z_)))));
    typename pythonic::assignable_noescape<decltype(z_[pythonic::numpy::functor::lexsort{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z_)), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z_)))])>::type z__ = z_[pythonic::numpy::functor::lexsort{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z_)), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z_)))];
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::le(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z__)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(z__))))>::type real_indices = pythonic::operator_::le(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z__)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(z__)));
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z__[real_indices]))>::type zr = pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z__[real_indices]);
    if (pythonic::operator_::eq(pythonic::builtins::functor::len{}(zr), pythonic::builtins::functor::len{}(z__)))
    {
      return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(std::integral_constant<long, 0>{}), pythonic::numpy::functor::float64{}), zr);
    }
    else
    {
      typename pythonic::assignable_noescape<decltype(z__[pythonic::operator_::invert(real_indices)])>::type z___ = z__[pythonic::operator_::invert(real_indices)];
      typename pythonic::assignable_noescape<decltype(z___.fast(pythonic::operator_::gt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L)))>::type zp = z___.fast(pythonic::operator_::gt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L));
      typename pythonic::assignable_noescape<decltype(z___.fast(pythonic::operator_::lt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L)))>::type zn = z___.fast(pythonic::operator_::lt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L));
      if (pythonic::operator_::ne(pythonic::builtins::functor::len{}(zp), pythonic::builtins::functor::len{}(zn)))
      {
        throw pythonic::builtins::functor::ValueError{}(pythonic::types::str("Array contains complex value without conjugate"));
      }
      typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::diff{}(pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename std::remove_cv<typename std::remove_reference<decltype(0L)>::type>::type>::type>>::type>::type({0L, pythonic::types::single_value()}), pythonic::operator_::le(pythonic::numpy::functor::diff{}(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, zp)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(zp[pythonic::types::contiguous_slice(pythonic::builtins::None,-1L)]))), typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename std::remove_cv<typename std::remove_reference<decltype(0L)>::type>::type>::type>>::type>::type({0L, pythonic::types::single_value()})))))>::type diffs = pythonic::numpy::functor::diff{}(pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename std::remove_cv<typename std::remove_reference<decltype(0L)>::type>::type>::type>>::type>::type({0L, pythonic::types::single_value()}), pythonic::operator_::le(pythonic::numpy::functor::diff{}(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, zp)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(zp[pythonic::types::contiguous_slice(pythonic::builtins::None,-1L)]))), typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename std::remove_cv<typename std::remove_reference<decltype(0L)>::type>::type>::type>>::type>::type({0L, pythonic::types::single_value()}))));
      typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::gt(diffs, 0L))))>::type run_starts = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::gt(diffs, 0L)));
      typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::lt(diffs, 0L))))>::type run_stops = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::lt(diffs, 0L)));
      {
        long  __target139918932098256 = pythonic::builtins::functor::len{}(run_starts);
        for (long  i=0L; i < __target139918932098256; i += 1L)
        {
          typename pythonic::assignable_noescape<decltype(run_starts.fast(i))>::type start = run_starts.fast(i);
          typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(run_stops.fast(i), 1L))>::type stop = pythonic::operator_::add(run_stops.fast(i), 1L);
          typename pythonic::assignable<typename __combined<__type28,__type35>::type>::type chunk = zp[pythonic::types::contiguous_slice(start,stop)];
          chunk[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = chunk[pythonic::numpy::functor::lexsort{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, chunk)))))];
          typename pythonic::assignable<typename __combined<__type38,__type44>::type>::type chunk_ = zn[pythonic::types::contiguous_slice(start,stop)];
          chunk_[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = chunk_[pythonic::numpy::functor::lexsort{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, chunk_)))))];
        }
      }
      return pythonic::types::make_tuple(pythonic::operator_::div(pythonic::operator_::add(zp, pythonic::numpy::functor::conj{}(zn)), 2L), zr);
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename zpk2tf::type<argument_type0, argument_type1, argument_type2>::result_type zpk2tf::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
  {
    return pythonic::types::make_tuple(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, pythonic::operator_::mul(k, poly()(z))), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, poly()(p)));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename zpk2sos::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type zpk2sos::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k, argument_type3&& n_sections) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef typename pythonic::lazy<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::append{})>::type>::type __type2;
    typedef long __type3;
    typedef decltype(std::declval<__type2>()(std::declval<__type1>(), std::declval<__type3>())) __type4;
    typedef typename pythonic::lazy<__type4>::type __type5;
    typedef typename __combined<__type1,__type5>::type __type6;
    typedef typename _cplxreal::type<__type6>::__ptype0 __type7;
    typedef typename __combined<__type5,__type7>::type __type8;
    typedef typename __combined<__type6,__type7>::type __type9;
    typedef typename _cplxreal::type<__type9>::__ptype1 __type10;
    typedef container<typename std::remove_reference<__type10>::type> __type11;
    typedef typename __combined<__type8,__type11>::type __type12;
    typedef typename __combined<__type1,__type12>::type __type13;
    typedef typename __combined<__type9,__type11>::type __type14;
    typedef typename __combined<__type13,__type14>::type __type15;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type16;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type16>(), std::declval<__type3>()))>::type __type17;
    typedef typename __combined<__type16,__type17>::type __type18;
    typedef typename _cplxreal::type<__type18>::__ptype0 __type19;
    typedef typename __combined<__type17,__type19>::type __type20;
    typedef typename __combined<__type18,__type19>::type __type21;
    typedef typename _cplxreal::type<__type21>::__ptype1 __type22;
    typedef container<typename std::remove_reference<__type22>::type> __type23;
    typedef typename __combined<__type20,__type23>::type __type24;
    typedef typename __combined<__type16,__type24>::type __type25;
    typedef typename __combined<__type21,__type23>::type __type26;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type27;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type28;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type29;
    typedef std::integral_constant<long, 6> __type30;
    typedef decltype(std::declval<__type28>()(std::declval<__type29>(), std::declval<__type30>())) __type31;
    typedef typename pythonic::assignable<decltype(std::declval<__type27>()(std::declval<__type31>()))>::type __type32;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type33;
    typedef decltype(std::declval<__type33>()(std::declval<__type29>())) __type34;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type __type35;
    typedef indexable<__type35> __type36;
    typedef typename __combined<__type32,__type36>::type __type37;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type38;
    typedef zpk2tf __type39;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros_like{})>::type>::type __type40;
    typedef std::integral_constant<long, 2> __type41;
    typedef decltype(std::declval<__type28>()(std::declval<__type29>(), std::declval<__type41>())) __type42;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type43;
    typedef typename pythonic::assignable<decltype(std::declval<__type27>()(std::declval<__type42>(), std::declval<__type43>()))>::type __type44;
    typedef typename pythonic::assignable<decltype(std::declval<__type40>()(std::declval<__type44>()))>::type __type45;
    typedef typename __combined<__type45,__type36>::type __type46;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type47;
    typedef _cplxreal __type48;
    typedef decltype(std::declval<__type48>()(std::declval<__type14>())) __type49;
    typedef typename pythonic::assignable<decltype(std::declval<__type38>()(std::declval<__type49>()))>::type __type50;
    typedef _nearest_real_complex_idx __type51;
    typedef decltype(std::declval<__type48>()(std::declval<__type26>())) __type52;
    typedef typename pythonic::assignable<decltype(std::declval<__type38>()(std::declval<__type52>()))>::type __type53;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argmin{})>::type>::type __type54;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type55;
    typedef decltype(std::declval<__type55>()(std::declval<__type53>())) __type56;
    typedef decltype(pythonic::operator_::sub(std::declval<__type3>(), std::declval<__type56>())) __type57;
    typedef decltype(std::declval<__type55>()(std::declval<__type57>())) __type58;
    typedef typename pythonic::assignable<decltype(std::declval<__type54>()(std::declval<__type58>()))>::type __type59;
    typedef typename pythonic::assignable<decltype(std::declval<__type53>()[std::declval<__type59>()])>::type __type60;
    typedef pythonic::types::str __type61;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type50>(), std::declval<__type60>(), std::declval<__type61>()))>::type __type62;
    typedef typename pythonic::assignable<decltype(std::declval<__type50>()[std::declval<__type62>()])>::type __type63;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::delete_{})>::type>::type __type64;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type50>(), std::declval<__type62>()))>::type __type65;
    typedef typename __combined<__type50,__type65>::type __type66;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type66>(), std::declval<__type60>(), std::declval<__type61>()))>::type __type67;
    typedef decltype(pythonic::operator_::sub(std::declval<__type60>(), std::declval<__type66>())) __type68;
    typedef decltype(std::declval<__type55>()(std::declval<__type68>())) __type69;
    typedef typename pythonic::assignable<decltype(std::declval<__type54>()(std::declval<__type69>()))>::type __type70;
    typedef typename __combined<__type67,__type70>::type __type71;
    typedef typename pythonic::assignable<decltype(std::declval<__type66>()[std::declval<__type71>()])>::type __type72;
    typedef typename __combined<__type63,__type72>::type __type73;
    typedef typename pythonic::assignable<long>::type __type74;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type75;
    typedef typename pythonic::assignable<decltype(std::declval<__type75>()(std::declval<__type73>()))>::type __type76;
    typedef typename __combined<__type74,__type76>::type __type77;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type66>(), std::declval<__type71>()))>::type __type78;
    typedef typename __combined<__type66,__type78>::type __type79;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type79>(), std::declval<__type60>(), std::declval<__type61>()))>::type __type80;
    typedef typename pythonic::assignable<decltype(std::declval<__type79>()[std::declval<__type80>()])>::type __type81;
    typedef typename __combined<__type77,__type81>::type __type82;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type79>(), std::declval<__type80>()))>::type __type83;
    typedef typename __combined<__type79,__type83>::type __type84;
    typedef typename pythonic::assignable<decltype(std::declval<__type75>()(std::declval<__type60>()))>::type __type85;
    typedef typename __combined<__type74,__type85>::type __type86;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type53>(), std::declval<__type59>()))>::type __type87;
    typedef typename __combined<__type53,__type87>::type __type88;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type88>(), std::declval<__type73>(), std::declval<__type61>()))>::type __type89;
    typedef typename pythonic::assignable<decltype(std::declval<__type88>()[std::declval<__type89>()])>::type __type90;
    typedef typename __combined<__type86,__type90>::type __type91;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type92;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type93;
    typedef decltype(std::declval<__type93>()(std::declval<__type88>())) __type94;
    typedef decltype(std::declval<__type92>()(std::declval<__type94>())) __type95;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type95>::type>::type>::type __type96;
    typedef decltype(std::declval<__type88>()[std::declval<__type96>()]) __type97;
    typedef decltype(std::declval<__type55>()(std::declval<__type97>())) __type98;
    typedef decltype(pythonic::operator_::sub(std::declval<__type98>(), std::declval<__type3>())) __type99;
    typedef decltype(std::declval<__type55>()(std::declval<__type99>())) __type100;
    typedef decltype(std::declval<__type54>()(std::declval<__type100>())) __type101;
    typedef typename pythonic::assignable<decltype(std::declval<__type96>()[std::declval<__type101>()])>::type __type102;
    typedef typename __combined<__type89,__type102>::type __type103;
    typedef typename pythonic::assignable<decltype(std::declval<__type88>()[std::declval<__type103>()])>::type __type104;
    typedef typename __combined<__type91,__type104>::type __type105;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type84>(), std::declval<__type105>(), std::declval<__type61>()))>::type __type106;
    typedef typename pythonic::assignable<decltype(std::declval<__type84>()[std::declval<__type106>()])>::type __type107;
    typedef typename __combined<__type82,__type107>::type __type108;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type73>(), std::declval<__type108>())) __type109;
    typedef decltype(std::declval<__type47>()(std::declval<__type109>())) __type110;
    typedef container<typename std::remove_reference<__type110>::type> __type111;
    typedef typename __combined<__type46,__type111>::type __type112;
    typedef pythonic::types::slice __type113;
    typedef typename pythonic::assignable<decltype(std::declval<__type112>()[std::declval<__type113>()])>::type __type114;
    typedef decltype(std::declval<__type114>()[std::declval<__type35>()]) __type115;
    typedef typename __combined<__type44,__type36>::type __type116;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type60>(), std::declval<__type105>())) __type117;
    typedef decltype(std::declval<__type47>()(std::declval<__type117>())) __type118;
    typedef container<typename std::remove_reference<__type118>::type> __type119;
    typedef typename __combined<__type116,__type119>::type __type120;
    typedef typename pythonic::assignable<decltype(std::declval<__type120>()[std::declval<__type113>()])>::type __type121;
    typedef decltype(std::declval<__type121>()[std::declval<__type35>()]) __type122;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type123;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type124;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type125;
    typedef decltype(std::declval<__type124>()(std::declval<__type125>())) __type126;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type126>())) __type127;
    typedef typename pythonic::assignable<decltype(std::declval<__type123>()(std::declval<__type29>(), std::declval<__type127>()))>::type __type128;
    typedef indexable<__type3> __type129;
    typedef typename __combined<__type128,__type129>::type __type130;
    typedef container<typename std::remove_reference<__type125>::type> __type131;
    typedef typename __combined<__type130,__type131>::type __type132;
    typedef decltype(std::declval<__type132>()[std::declval<__type35>()]) __type133;
    typedef decltype(std::declval<__type39>()(std::declval<__type115>(), std::declval<__type122>(), std::declval<__type133>())) __type134;
    typedef decltype(std::declval<__type38>()(std::declval<__type134>())) __type135;
    typedef container<typename std::remove_reference<__type135>::type> __type136;
    typedef typename __combined<__type37,__type136>::type __type137;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type84>(), std::declval<__type106>()))>::type __type138;
    typedef typename pythonic::assignable<decltype(std::declval<__type64>()(std::declval<__type88>(), std::declval<__type103>()))>::type __type139;
    typename pythonic::assignable<typename __combined<__type82,__type107>::type>::type z2;
    typename pythonic::assignable<typename __combined<__type91,__type104>::type>::type p2;
    typename pythonic::assignable<typename __combined<__type89,__type102>::type>::type p2_idx;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type>::type si_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type>::type si;
    typename pythonic::assignable<typename __combined<__type63,__type72>::type>::type z1;
    typename pythonic::lazy<__type15>::type z_ = z;
    typename pythonic::assignable<typename __combined<__type25,__type26>::type>::type p_ = p;
    typename pythonic::assignable<typename __combined<__type137,__type36>::type>::type sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(n_sections, std::integral_constant<long, 6>{}));
    if (pythonic::operator_::eq(pythonic::operator_::mod(pythonic::builtins::functor::len{}(p_), 2L), 1L))
    {
      p_ = pythonic::numpy::functor::append{}(p_, 0L);
      z_ = pythonic::numpy::functor::append{}(z_, 0L);
    }
    typename pythonic::assignable<typename __combined<__type84,__type138>::type>::type z__ = pythonic::numpy::functor::concatenate{}(_cplxreal()(z_));
    typename pythonic::assignable<typename __combined<__type88,__type139>::type>::type p__ = pythonic::numpy::functor::concatenate{}(_cplxreal()(p_));
    typename pythonic::assignable<typename __combined<__type120,__type36>::type>::type p_sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(n_sections, std::integral_constant<long, 2>{}), pythonic::numpy::functor::complex128{});
    typename pythonic::assignable<typename __combined<__type112,__type36>::type>::type z_sos = pythonic::numpy::functor::zeros_like{}(p_sos);
    {
      long  __target139918932205184 = n_sections;
      for (long  si=0L; si < __target139918932205184; si += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(1L, pythonic::numpy::functor::abs{}(p__)))))>::type p1_idx = pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(1L, pythonic::numpy::functor::abs{}(p__))));
        typename pythonic::assignable_noescape<decltype(p__[p1_idx])>::type p1 = p__[p1_idx];
        p__ = pythonic::numpy::functor::delete_{}(p__, p1_idx);
        {
          typename pythonic::assignable<typename __combined<__type67,__type70>::type>::type z1_idx_;
          if (pythonic::builtins::pythran::and_([&] () { return pythonic::numpy::functor::isreal{}(p1); }, [&] () { return pythonic::operator_::eq(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::isreal{}(p__)), 0L); }))
          {
            typename pythonic::assignable_noescape<decltype(_nearest_real_complex_idx()(z__, p1, pythonic::types::str("real")))>::type z1_idx = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("real"));
            z1 = z__[z1_idx];
            z__ = pythonic::numpy::functor::delete_{}(z__, z1_idx);
            p2= z2 = 0L;
          }
          else
          {
            if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(p1)); }, [&] () { return pythonic::operator_::eq(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::isreal{}(z__)), 1L); }))
            {
              z1_idx_ = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("complex"));
              pythonic::pythran_assert(pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z__[z1_idx_])));
            }
            else
            {
              z1_idx_ = pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(p1, z__)));
            }
            z1 = z__[z1_idx_];
            z__ = pythonic::numpy::functor::delete_{}(z__, z1_idx_);
            if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(p1)))
            {
              {
                typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type79>(), std::declval<__type60>(), std::declval<__type61>()))>::type>::type z2_idx;
                if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z1)))
                {
                  p2 = pythonic::numpy::functor::conj{}(p1);
                  z2 = pythonic::numpy::functor::conj{}(z1);
                }
                else
                {
                  p2 = pythonic::numpy::functor::conj{}(p1);
                  z2_idx = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("real"));
                  z2 = z__[z2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(z2));
                  z__ = pythonic::numpy::functor::delete_{}(z__, z2_idx);
                }
              }
            }
            else
            {
              {
                typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type95>::type>::type>::type>::type idx;
                typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type51>()(std::declval<__type84>(), std::declval<__type105>(), std::declval<__type61>()))>::type>::type z2_idx_;
                if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z1)))
                {
                  z2 = pythonic::numpy::functor::conj{}(z1);
                  p2_idx = _nearest_real_complex_idx()(p__, z1, pythonic::types::str("real"));
                  p2 = p__[p2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(p2));
                }
                else
                {
                  idx = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::numpy::functor::isreal{}(p__)));
                  pythonic::pythran_assert(pythonic::operator_::gt(pythonic::builtins::functor::len{}(idx), 0L));
                  p2_idx = idx[pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(pythonic::numpy::functor::abs{}(p__[idx]), 1L)))];
                  p2 = p__[p2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(p2));
                  z2_idx_ = _nearest_real_complex_idx()(z__, p2, pythonic::types::str("real"));
                  z2 = z__[z2_idx_];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(z2));
                  z__ = pythonic::numpy::functor::delete_{}(z__, z2_idx_);
                }
              }
              p__ = pythonic::numpy::functor::delete_{}(p__, p2_idx);
            }
          }
        }
        p_sos[si] = pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(p1, p2));
        z_sos[si] = pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(z1, z2));
      }
    }
    pythonic::pythran_assert(pythonic::operator_::eq(pythonic::builtins::functor::len{}(p__), pythonic::builtins::functor::len{}(z__)) and pythonic::operator_::eq(pythonic::builtins::functor::len{}(z__), 0L));
    
    typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type120>()[std::declval<__type113>()])>::type>::type p_sos_ = p_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)];
    typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type112>()[std::declval<__type113>()])>::type>::type z_sos_ = z_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)];
    typename pythonic::assignable<typename __combined<__type132,__type129>::type>::type gains = pythonic::numpy::functor::ones{}(n_sections, pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::numpy::functor::array{}(k)));
    std::get<0>(gains) = k;
    {
      long  __target139918931838336 = n_sections;
      for (long  si_=0L; si_ < __target139918931838336; si_ += 1L)
      {
        sos[si_] = pythonic::numpy::functor::concatenate{}(zpk2tf()(z_sos_[si_], p_sos_[si_], gains[si_]));
      }
    }
    return sos;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename zpk2sos_multiple::type<argument_type0, argument_type1, argument_type2>::result_type zpk2sos_multiple::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type0;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type4;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type5;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type5>())) __type6;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
    typedef decltype(pythonic::operator_::sub(std::declval<__type7>(), std::declval<__type9>())) __type10;
    typedef long __type11;
    typedef typename __combined<__type10,__type11>::type __type12;
    typedef decltype(std::declval<__type4>()(std::declval<__type12>(), std::declval<__type11>())) __type13;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type14;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type15;
    typedef typename pythonic::assignable<decltype(std::declval<__type14>()(std::declval<__type15>()))>::type __type16;
    typedef decltype(std::declval<__type3>()(std::declval<__type13>(), std::declval<__type16>())) __type17;
    typedef decltype(std::declval<__type2>()(std::declval<__type17>())) __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type18>())) __type19;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type19>(), std::declval<__type11>()))>::type __type20;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type20>())) __type21;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type __type22;
    typedef decltype(pythonic::operator_::sub(std::declval<__type22>(), std::declval<__type7>())) __type23;
    typedef typename __combined<__type23,__type11>::type __type24;
    typedef decltype(std::declval<__type4>()(std::declval<__type24>(), std::declval<__type11>())) __type25;
    typedef decltype(std::declval<__type3>()(std::declval<__type25>(), std::declval<__type16>())) __type26;
    typedef decltype(std::declval<__type2>()(std::declval<__type26>())) __type27;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type27>())) __type28;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type28>(), std::declval<__type11>()))>::type __type29;
    typedef pythonic::types::contiguous_slice __type30;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type31;
    typedef decltype(std::declval<__type31>()(std::declval<__type16>())) __type32;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
    typedef decltype(std::declval<__type29>()(std::declval<__type30>(), std::declval<__type33>())) __type34;
    typedef decltype(std::declval<__type20>()(std::declval<__type30>(), std::declval<__type33>())) __type35;
    typedef decltype(std::declval<__type15>()[std::declval<__type33>()]) __type36;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type29>())) __type37;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type37>::type>::type __type38;
    typedef typename __combined<__type22,__type38>::type __type39;
    typedef decltype(std::declval<__type4>()(std::declval<__type39>(), std::declval<__type38>())) __type40;
    typedef decltype(pythonic::operator_::add(std::declval<__type40>(), std::declval<__type11>())) __type41;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type41>(), std::declval<__type11>()))>::type __type42;
    typedef typename zpk2sos::type<__type34, __type35, __type36, __type42>::__ptype3 __type43;
    typedef container<typename std::remove_reference<__type43>::type> __type44;
    typedef typename zpk2sos::type<__type34, __type35, __type36, __type42>::__ptype2 __type45;
    typedef container<typename std::remove_reference<__type45>::type> __type46;
    typedef std::integral_constant<long, 6> __type47;
    typedef decltype(std::declval<__type3>()(std::declval<__type16>(), std::declval<__type42>(), std::declval<__type47>())) __type48;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type48>()))>::type __type49;
    typedef zpk2sos __type50;
    typedef decltype(std::declval<__type50>()(std::declval<__type34>(), std::declval<__type35>(), std::declval<__type36>(), std::declval<__type42>())) __type51;
    typedef container<typename std::remove_reference<__type51>::type> __type52;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type>::type filt;
    typename pythonic::assignable_noescape<decltype(z)>::type z_ = z;
    typename pythonic::assignable_noescape<decltype(p)>::type p_ = p;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(k))>::type nfilt = pythonic::builtins::functor::len{}(k);
    pythonic::pythran_assert(pythonic::operator_::eq(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_))) and pythonic::operator_::eq(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_)), nfilt));
    typename pythonic::assignable<typename __combined<__type20,__type44>::type>::type p__ = pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(p_, pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::builtins::functor::max{}(pythonic::operator_::sub(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_))), 0L), nfilt))), 0L);
    typename pythonic::assignable<typename __combined<__type29,__type46>::type>::type z__ = pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(z_, pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::builtins::functor::max{}(pythonic::operator_::sub(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_))), 0L), nfilt))), 0L);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::add(pythonic::builtins::functor::max{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z__))), 1L), 2L))>::type n_sections = pythonic::operator_::functor::floordiv()(pythonic::operator_::add(pythonic::builtins::functor::max{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z__))), 1L), 2L);
    typename pythonic::assignable<typename __combined<__type49,__type52>::type>::type sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nfilt, n_sections, std::integral_constant<long, 6>{}));
    {
      long  __target139918931871872 = nfilt;
      for (long  filt=0L; filt < __target139918931871872; filt += 1L)
      {
        sos(filt,pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)) = zpk2sos()(z__(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),filt), p__(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),filt), k[filt], n_sections);
      }
    }
    return sos;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& z, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple1(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& z, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& z, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& z, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran__zpk_funcs::_cplxreal::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type _cplxreal0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& z) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::_cplxreal()(z);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_zpk2sos_multiple0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple1(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__cplxreal0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"z",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[0]))
        return to_python(_cplxreal0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_zpk2sos_multiple(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_zpk2sos_multiple0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "zpk2sos_multiple", "\n""    - zpk2sos_multiple(complex[:,:], complex[:,:], float[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__cplxreal(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__cplxreal0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_cplxreal", "\n""    - _cplxreal(complex[:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "zpk2sos_multiple",
    (PyCFunction)__pythran_wrapall_zpk2sos_multiple,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - zpk2sos_multiple(complex[:,:], complex[:,:], float[:])"},{
    "_cplxreal",
    (PyCFunction)__pythran_wrapall__cplxreal,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - _cplxreal(complex[:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_zpk_funcs",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_zpk_funcs)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_zpk_funcs)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_zpk_funcs",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.9.dev",
                                      "2021-03-30 11:58:38.846230",
                                      "b899aad88a57e48712df1ad0823acfa35403746bfe70efe19a440548a5712797");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif