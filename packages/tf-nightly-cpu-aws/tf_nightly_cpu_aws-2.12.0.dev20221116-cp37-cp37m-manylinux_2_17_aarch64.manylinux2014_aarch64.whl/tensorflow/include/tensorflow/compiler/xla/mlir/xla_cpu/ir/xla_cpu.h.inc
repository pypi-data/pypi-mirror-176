/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace xla_cpu {
class AllReduceOp;
} // namespace xla_cpu
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::AllReduceOp declarations
//===----------------------------------------------------------------------===//

class AllReduceOpAdaptor {
public:
  AllReduceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  AllReduceOpAdaptor(AllReduceOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getOperand();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  ::mlir::UnitAttr getUseGlobalDeviceIdsAttr();
  bool getUseGlobalDeviceIds();
  ::mlir::IntegerAttr getReductionKindAttr();
  ::llvm::APInt getReductionKind();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class AllReduceOp : public ::mlir::Op<AllReduceOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::OpTrait::SameOperandsElementType, ::mlir::OpTrait::SameOperandsAndResultType> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllReduceOpAdaptor;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("channel_handle"), ::llvm::StringRef("reduction_kind"), ::llvm::StringRef("replica_groups"), ::llvm::StringRef("use_global_device_ids")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getChannelHandleAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getChannelHandleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getReductionKindAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getReductionKindAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getReplicaGroupsAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getReplicaGroupsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getUseGlobalDeviceIdsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getUseGlobalDeviceIdsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.all_reduce");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getOperand();
  ::mlir::MutableOperandRange getOperandMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  ::mlir::UnitAttr getUseGlobalDeviceIdsAttr();
  bool getUseGlobalDeviceIds();
  ::mlir::IntegerAttr getReductionKindAttr();
  ::llvm::APInt getReductionKind();
  void setReplicaGroupsAttr(::mlir::DenseIntElementsAttr attr);
  void setChannelHandleAttr(::mlir::IntegerAttr attr);
  void setChannelHandle(uint64_t attrValue);
  void setUseGlobalDeviceIdsAttr(::mlir::UnitAttr attr);
  void setUseGlobalDeviceIds(bool attrValue);
  void setReductionKindAttr(::mlir::IntegerAttr attr);
  void setReductionKind(::llvm::APInt attrValue);
  ::mlir::Attribute removeUse_global_device_idsAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::ValueRange operand, ::mlir::DenseIntElementsAttr replica_groups, ::mlir::IntegerAttr channel_handle, /*optional*/::mlir::UnitAttr use_global_device_ids, ::mlir::IntegerAttr reduction_kind);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::ValueRange operand, ::mlir::DenseIntElementsAttr replica_groups, uint64_t channel_handle, /*optional*/bool use_global_device_ids, ::llvm::APInt reduction_kind);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::AllReduceOp)


#endif  // GET_OP_CLASSES

