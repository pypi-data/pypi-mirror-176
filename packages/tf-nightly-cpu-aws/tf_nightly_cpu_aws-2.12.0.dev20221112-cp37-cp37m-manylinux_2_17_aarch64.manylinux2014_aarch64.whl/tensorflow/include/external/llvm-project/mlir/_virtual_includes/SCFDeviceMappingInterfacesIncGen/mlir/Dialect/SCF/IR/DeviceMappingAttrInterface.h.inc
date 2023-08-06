/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
class DeviceMappingAttrInterface;
namespace detail {
struct DeviceMappingAttrInterfaceInterfaceTraits {
  struct Concept {
  };
  template<typename ConcreteAttr>
  class Model : public Concept {
  public:
    using Interface = ::mlir::DeviceMappingAttrInterface;
    Model() : Concept{} {}

  };
  template<typename ConcreteAttr>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::DeviceMappingAttrInterface;
    FallbackModel() : Concept{} {}

  };
  template<typename ConcreteModel, typename ConcreteAttr>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteAttr;
  };
};template <typename ConcreteAttr>
struct DeviceMappingAttrInterfaceTrait;

} // namespace detail
class DeviceMappingAttrInterface : public ::mlir::AttributeInterface<DeviceMappingAttrInterface, detail::DeviceMappingAttrInterfaceInterfaceTraits> {
public:
  using ::mlir::AttributeInterface<DeviceMappingAttrInterface, detail::DeviceMappingAttrInterfaceInterfaceTraits>::AttributeInterface;
  template <typename ConcreteAttr>
  struct Trait : public detail::DeviceMappingAttrInterfaceTrait<ConcreteAttr> {};
};
namespace detail {
  template <typename ConcreteAttr>
  struct DeviceMappingAttrInterfaceTrait : public ::mlir::AttributeInterface<DeviceMappingAttrInterface, detail::DeviceMappingAttrInterfaceInterfaceTraits>::Trait<ConcreteAttr> {
  };
}// namespace detail
} // namespace mlir
namespace mlir {
} // namespace mlir
